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
    messages = [ #defines the role of chat 
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
                    {'userID':'72', 'compatibility_score': 75,'reasoning':'you share favorite artists and genres, showing strong compatibility. your similar tastes suggest you would enjoy each other's playlists. Recommended artists based on their data: (provide recommendations ). (Keep reasoning ~30 words)'}
                ]
                """}]    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users_music_data WHERE user_id = %s", (ref_user_id,))
        reference_user = cursor.fetchone()
        user_ids = [reference_user["user_id"]] #init user_ids with ref user as 1st entry

        if not reference_user:
            return jsonify({"error": "Could not get your Profile."}), 404

        cursor.execute("SELECT COUNT(*) AS user_count FROM users_music_data")
        result = cursor.fetchone() 

        if result is None or "user_count" not in result:
            return jsonify({"error": "Could not retrieve user count."}), 500

        user_count = int(result["user_count"]) - 1 #gets number of users in table - ref user
        offset = 0

        while offset < user_count:
            cursor.execute(f"SELECT * FROM users_music_data LIMIT 5 OFFSET {offset}") #gets first 5 users, then increments until end of list
            rows = cursor.fetchall()
            user_ids.extend([row["user_id"] for row in rows if row["user_id"] != ref_user_id]) #doesnt add ref user
            if not user_ids:
                return jsonify({"error": "No other users found for comparison"}), 404
            users_data = []
            for user_id in user_ids:
                cursor.execute("SELECT * FROM users_music_data WHERE user_id = %s", (user_id,)) 
                user_row = cursor.fetchone()
                if not user_row:
                    continue  

                users_data.append({ #adds song data
                    "userid": user_row["user_id"],
                    "topSongs": user_row["top_songs"],
                    "topArtists": user_row["top_artists"],
                    "topGenres": user_row["top_genres"]
                })

            offset += (len(users_data)-1) #offset for next sql query
            message_content = json.dumps(users_data)
            messages.append({"role": "user", "content": message_content})
            chat = client.beta.chat.completions.parse(
                model="gpt-3.5-turbo",
                messages=messages,
                response_format={"type": "json_object"}
            )

            reply = chat.choices[0].message.content
            insert_response(reply,ref_user_id)
            user_ids = [ref_user_id] #reset user_ids
            if len(messages) > 1:
                del messages[1]
        cursor.close()
        conn.close()
        return jsonify(json.loads(reply))
    
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500

    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


def insert_response(reply,ref_user_id):
    try:
        matches_data = json.loads(reply).get("matches", [])

        if not matches_data:
            print("No matches found.")
            return

        conn = get_db_connection()
        if conn is None:
            print("Unable to connect to the database.")
            return

        cursor = conn.cursor()

        for match in matches_data:
            user_id = match["userID"]
            compatibility_score = match["compatibility_score"]
            reasoning = match["reasoning"]


            cursor.execute("""
                INSERT INTO matches (match_id, user_1_id, user_2_id, match_score, status, reasoning)
                VALUES (UUID(), %s, %s, %s, 'pending',%s)
            """, (ref_user_id, user_id, compatibility_score,reasoning))

        conn.commit()
        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"Database error: {err}")

    except json.JSONDecodeError as err:
        print(f"JSON parsing error: {err}")