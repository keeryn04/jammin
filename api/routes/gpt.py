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

def find_common_elements(list1, list2):
    """Helper function to find common elements between two lists."""
    set1 = set(list1)
    set2 = set(list2)
    return list(set1.intersection(set2))

@openai_routes.route("/chattesting/<ref_user_id>", methods=["GET"])
def run_ChatQuery(ref_user_id):
    messages = [
        {"role": "system", "content": 
         """You are a matchmaking compatibility score generator for music preferences. You will be given a list of users, each with their favorite songs, artists, and genres. 
         The first user in the list is the REFERENCE user. You will match them with ALL others (not self!) and EXCLUDE the user themselves from the output. You will identify common top songs and artists between the reference user and each other user, and prioritize top genres when giving a compatibility score. Be generous with scores.
         The output should be in JSON format and include the profile_name, common_top_songs, and common_top_artists of the matched user. Make sure to return JSONs for every user you receive.
         Example input:
         [
         {'userid':'0', 'profile_name': 'Tony Stark', 'topSongs':['SongA', 'SongB'], 'topArtists':['ArtistA', 'ArtistB'], 'topGenres':['GenreA']},
         {'userid':'72', 'profile_name': 'Thor', 'topSongs':['SongB', 'SongC'], 'topArtists':['ArtistB', 'ArtistC'], 'topGenres':['GenreB']}
         ]
         Example output:
         {
           "matches": [
             {
               "userID": "72",
               "profile_name": "Thor",
               "compatibility_score": 75,
               "reasoning": "You and *insert profile_name* share favorite artists and genres (provide example if they do), showing strong compatibility. Your similar tastes suggest you would enjoy each other's playlists. Recommended artists: (provide recommendations based on both their top genres). (Keep reasoning ~30 words)",
               "common_top_songs": ["SongB"],
               "common_top_artists": ["ArtistB"]
             }
           ]
         }
         """}
    ]

    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500

        cursor = conn.cursor(dictionary=True)
        
        # Fetch the reference user
        cursor.execute("SELECT * FROM users_music_data WHERE user_data_id = %s", (ref_user_id,))
        reference_user = cursor.fetchone()

        if not reference_user:
            return jsonify({"error": "Could not get your Profile."}), 404

        # Fetch all users excluding the reference user
        cursor.execute("SELECT * FROM users_music_data WHERE user_data_id != %s", (ref_user_id,))
        rows = cursor.fetchall()

        if not rows:
            return jsonify({"error": "No other users found for comparison"}), 404

        # Prepare the data for the LLM
        users_data = []
        for row in rows:
            users_data.append({
                "userid": row["user_data_id"],
                "profile_name": row["profile_name"],
                "topSongs": row["top_songs"].split(", "),  # Pass raw data
                "topArtists": row["top_artists"].split(", "),  # Pass raw data
                "topGenres": row["top_genres"].split(", ")  # Pass raw data
            })

        # Include the reference user in the data sent to the LLM
        users_data.insert(0, {
            "userid": reference_user["user_data_id"],
            "profile_name": reference_user["profile_name"],
            "topSongs": reference_user["top_songs"].split(", "),  # Pass raw data
            "topArtists": reference_user["top_artists"].split(", "),  # Pass raw data
            "topGenres": reference_user["top_genres"].split(", ")  # Pass raw data
        })

        print("Users Data Sent to LLM:", users_data)  # Log input data

        message_content = json.dumps(users_data)
        messages.append({"role": "user", "content": message_content})

        # Call the LLM
        chat = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            response_format={"type": "json_object"}
        )

        reply = chat.choices[0].message.content
        print("LLM Response:", reply)  # Log the LLM's response

        insert_response(reply, ref_user_id)

        cursor.close()
        conn.close()
        return jsonify(json.loads(reply))

    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500

    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


def insert_response(reply, ref_user_id):
    try:
        print("LLM Response:", reply)  # Log the LLM's response
        matches_data = json.loads(reply).get("matches", [])
        print(f"Number of matches returned by LLM: {len(matches_data)}")  # Log the number of matches

        if not matches_data:
            print("No matches found.")
            return

        conn = get_db_connection()
        if conn is None:
            print("Unable to connect to the database.")
            return

        cursor = conn.cursor()
        inserted_count = 0
        skipped_count = 0

        for match in matches_data:
            user_id = match.get("userID")
            compatibility_score = match.get("compatibility_score")
            reasoning = match.get("reasoning")

            # Validate data
            if not all([user_id, compatibility_score, reasoning]):
                print(f"Skipping invalid match data: {match}")
                skipped_count += 1
                continue

            # Log the data being inserted
            print(f"Inserting match: user_1_id={ref_user_id}, user_2_id={user_id}, match_score={compatibility_score}, reasoning={reasoning}")

            try:
                cursor.execute("""
                    INSERT INTO matches (match_id, user_1_id, user_2_id, match_score, reasoning, status)
                    VALUES (UUID(), %s, %s, %s, %s, 'pending')
                    ON DUPLICATE KEY UPDATE 
                    match_score = VALUES(match_score), 
                    status = 'pending', 
                    reasoning = VALUES(reasoning);
                """, (ref_user_id, user_id, compatibility_score, reasoning))
                inserted_count += 1
            except mysql.connector.Error as err:
                print(f"Database error for match {user_id}: {err}")
                skipped_count += 1

        conn.commit()
        cursor.close()
        conn.close()

        print(f"Inserted {inserted_count} matches, skipped {skipped_count} matches.")

    except json.JSONDecodeError as err:
        print(f"JSON parsing error: {err}")
    except Exception as e:
        print(f"Unexpected error in insert_response: {str(e)}")