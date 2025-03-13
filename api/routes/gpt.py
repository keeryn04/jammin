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

@openai_routes.route("/api/chattesting/<ref_user_id>", methods=["GET"])
def run_ChatQuery(ref_user_id):
    messages = [ #defines the role of chat 
                {"role": "system", "content": 
                """You are a matchmaking compatibility score generator for music preferences. You will be given a list of users, each with their favorite songs, artists, and genres. 
                The first user in the list is the REFERENCE user. You will match them with all others and EXCLUDE them from the output. You Will prioritize top genres when giving a compatibility score, and be generous with scores.
                The output should be in JSON format.
                Example input:
                [
                {'userid':'0', 'topSongs':['SongA'], 'topArtists':['ArtistA'], 'topGenres':['GenreA']},
                {'userid':'72', 'topSongs':['SongB'], 'topArtists':['ArtistB'], 'topGenres':['GenreB']}
                ]
                Example output:
                [
                    {'userID':'72', 'compatibility_score': 75,'reasoning':'you share favorite artists and genres (provide example if they do), showing strong compatibility. your similar tastes suggest you would enjoy each other's playlists. Recommended artists: (provide recommendations based on both their top genres). (Keep reasoning ~30 words)'}
                ]
                """}]    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500
        
        response = conn.table("users_music_data").select("*").eq("user_id", ref_user_id).execute()

        if not reference_user:
            return jsonify({"error": "Could not get your Profile."}), 404
        
        reference_user = response.data[0]  # Grab first user as reference user
        user_ids = [reference_user["user_id"]]

        result = conn.table("users_music_data").select("COUNT(*)", count="exact").execute()
        user_count = result.count

        if not user_count:
            return jsonify({"error": "Could not retrieve user count."}), 500

        user_count = user_count - 1 #gets number of users in table - ref user
        offset = 0

        while offset < user_count:
            rows = conn.table("users_music_data").select("*").limit(5).offset(offset).execute() #gets first 5 users, then increments until end of list
            user_ids.extend([row["user_id"] for row in rows if row["user_id"] != ref_user_id]) #doesnt add ref user

            if not user_ids:
                return jsonify({"error": "No other users found for comparison"}), 404
            
            users_data = []
            for user_id in user_ids:
                rows = conn.table("users_music_data").select("*").eq("user_id", user_id).limit(5).offset(offset).execute()
                user_row = rows[0]

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

            match_id = str(uuid.uuid4)

            data = {
                "match_id": match_id,  
                "user_1_id": ref_user_id,
                "user_2_id": user_id,
                "match_score": compatibility_score,
                "status": "pending",
                "reasoning": reasoning
            }

            #Insert into the table with upsert behavior
            response = conn.table("matches").upsert(data, on_conflict=["match_id"]).execute()

            if response.error:
                return jsonify({"error": "Failed to insert or update match.", "details": response.error.message}), 500

    except mysql.connector.Error as err:
        print(f"Database error: {err}")

    except json.JSONDecodeError as err:
        print(f"JSON parsing error: {err}")