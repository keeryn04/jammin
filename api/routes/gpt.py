from flask import Blueprint, app, jsonify, request, session, redirect, url_for
from flask_cors import CORS
from spotipy.oauth2 import SpotifyOAuth
import mysql.connector
import os
import requests
from dotenv import load_dotenv
import uuid
import openai
import json

load_dotenv()
from database_connector import get_db_connection

API_ACCESS_KEY = os.getenv('API_ACCESS_KEY', 'key')
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=openai.api_key)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
openai_routes = Blueprint("openai_routes", __name__)

def require_api_key(f):
    def decorated_function(*args, **kwargs):
        api_key = request.args.get("api_key")
        if api_key != API_ACCESS_KEY:
            return jsonify({"error": "Unauthorized"}), 403
        return f(*args, **kwargs)
    return decorated_function

@openai_routes.route("/chattesting/<ref_user_id>", methods=["GET"])
def run_ChatQuery(ref_user_id):    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users_music_data WHERE profile_name != %s LIMIT 5",(ref_user_id,))
        user_ids = [row["user_id"] for row in cursor.fetchall()]

        if not user_ids:
            return jsonify({"error": "No other users found for comparison"}), 404
        users_data = []

        for user_id in user_ids:
            cursor.execute("SELECT * FROM users_music_data WHERE user_id = %s", (user_id,))
            user_row = cursor.fetchone()
            if not user_row:
                continue  # Skip if user not found

            users_data.append({
                "userid": user_row["user_id"],
                "topSongs": user_row["top_songs"],
                "topArtists": user_row["top_artists"],
                "topGenres": user_row["top_genres"]
            })
        cursor.close()
        conn.close()
        messages = [ #defines the role of
            {"role": "system", "content": 
            """You are a matchmaking compatibility score generator for music preferences. You will be given a list of users, each with their favorite songs, artists, and genres. 
            The first user in the list is the REFERENCE user. You will match them with all others and EXCLUDE them from the output.
            The output should be in JSON format.
            Example input:
            [
            {'userid':'0', 'topSongs':['SongA'], 'topArtists':['ArtistA'], 'topGenres':['GenreA']},
            {'userid':'72', 'topSongs':['SongB'], 'topArtists':['ArtistB'], 'topGenres':['GenreB']}
            ]
            Example output:
            [
                {'userID':'72', 'compatibility_score': 75,'reasoning':'They share multiple favorite artists (list artists) and have a strong overlap in their preferred music genres (list genres), indicating a high level of musical compatibility. Their listening habits suggest similar tastes and influences, making them likely to enjoy each other's playlists and discover new music together. They might like these Artists: (provide a reccomendation based on their data)'}
            ]
            """}]
        
        message_content = json.dumps(users_data)
        messages.append({"role": "user", "content": message_content})
        chat = client.beta.chat.completions.parse(
            model="gpt-3.5-turbo",
            messages=messages,
            response_format={"type": "json_object"}
        )
        reply = chat.choices[0].message.content
        insert_response(reply,ref_user_id)
        return jsonify(json.loads(reply))
    
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500

    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


def insert_response(reply,ref_user_id):
    try:
        # Parse the reply JSON
        matches_data = json.loads(reply).get("matches", [])

        if not matches_data:
            print("No matches found.")
            return

        # Connect to the database
        conn = get_db_connection()
        if conn is None:
            print("Unable to connect to the database.")
            return

        cursor = conn.cursor()

        # Insert data into the matches table
        for match in matches_data:
            user_id = match["userID"]
            compatibility_score = match["compatibility_score"]


            cursor.execute("""
                INSERT INTO matches (match_id, user_1_id, user_2_id, match_score, status)
                VALUES (UUID(), %s, %s, %s, 'pending')
            """, (ref_user_id, user_id, compatibility_score))

        # Commit the transaction
        conn.commit()
        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"Database error: {err}")

    except json.JSONDecodeError as err:
        print(f"JSON parsing error: {err}")