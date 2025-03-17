from flask import Blueprint, app, jsonify, request, session, redirect, url_for
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv
import uuid
import openai
import json

load_dotenv()
from api.database_connector import get_db_connection
from api.routes.users import get_user_id_by_user_data_id

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

@openai_routes.route("/api/chattesting/<ref_user_data_id>", methods=["GET"])
def run_ChatQuery(ref_user_data_id):
    messages = [
        {"role": "system", "content": 
         """You are a matchmaking compatibility score generator for music preferences. You will be given a list of users, each with their favorite songs, artists, and genres. 
         The first user in the list is the REFERENCE user. You will match them with ALL others (not self!) and EXCLUDE the user themselves from the output. You will identify common top songs and artists between the reference user and each other user, and prioritize top genres when giving a compatibility score. Be generous with scores.
         The output should be in JSON format and include the profile_name, common_top_songs, and common_top_artists of the matched user. Make sure to return JSONs for every user you receive.
         Example input:
         [
         {'user_id':'126', 'user_data_id':'0', 'profile_name': 'Tony Stark', 'topSongs':['SongA', 'SongB'], 'topArtists':['ArtistA', 'ArtistB'], 'topGenres':['GenreA']},
         {'user_id':'130', 'user_data_id':'72', 'profile_name': 'Thor', 'topSongs':['SongB', 'SongC'], 'topArtists':['ArtistB', 'ArtistC'], 'topGenres':['GenreB']}
         ]
         Example output:
         {
           "matches": [
             {
               "user_id": "130",
               "user_data_id": "72",
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

        #Grab user with user_data_id as reference user
        response = conn.table("users_music_data").select("*").eq("user_data_id", ref_user_data_id).execute()

        if not response.data:
            return jsonify({"error": "Could not get your Profile."}), 404
        
        reference_user = response.data[0]

        response = conn.table("users_music_data").select("*").neq("user_data_id", ref_user_data_id).execute()
        other_users = response.data

        if not other_users:
             return jsonify({"error": "No other users found for comparison"}), 404
        
        #Fetch all matches
        matches_response = conn.table("matches").select("*").execute()
        matches_data = matches_response.data

        #Fetch reference users ID
        ref_user_id_response = get_user_id_by_user_data_id(ref_user_data_id)
        ref_user_id_json = ref_user_id_response.get_json()
        ref_user_id = ref_user_id_json.get("user_id")

        users_data = []
        for user in other_users:
            #Fetch 2nd user's ID, and check if a match between reference and new user exists
            user_2_id_response = get_user_id_by_user_data_id(user["user_data_id"])
            user_2_id_json = user_2_id_response.get_json()
            user_2_id = user_2_id_json.get("user_id")

            existing_match = next(
                (match for match in matches_data if 
                    ((match.get("user_1_id") == ref_user_id and match.get("user_2_id") == user_2_id) or
                    (match.get("user_1_id") == user_2_id and match.get("user_2_id") == ref_user_id))),
                None
            )

            #Match doesn't exist, create a new entry
            if not existing_match or existing_match["status"] == "pending":
                users_data.append({
                    "user_id": user_2_id,
                    "user_data_id": user["user_data_id"],
                    "profile_name": user["profile_name"],
                    "topSongs": user["top_songs"].split(", "),
                    "topArtists": user["top_artists"].split(", "),
                    "topGenres": user["top_genres"].split(", ")
                })
        
        #Include the reference user in the data sent to the LLM
        users_data.insert(0, {
            "user_id": ref_user_id,
            "user_data_id": reference_user["user_data_id"],
            "profile_name": reference_user["profile_name"],
             "topSongs": reference_user["top_songs"].split(", "),
             "topArtists": reference_user["top_artists"].split(", "),
             "topGenres": reference_user["top_genres"].split(", ")
        })

        #Create info to send to LLM
        message_content = json.dumps(users_data)
        messages.append({"role": "user", "content": message_content})

        #Call the LLM
        chat = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            response_format={"type": "json_object"}
        )

        #Receive reply and update database
        reply = chat.choices[0].message.content
        insert_response(reply, ref_user_id)

        return jsonify(json.loads(reply))

    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

def insert_response(reply, ref_user_id):
    try:
        #Retrieve data from LLM
        matches_data = json.loads(reply).get("matches", [])

        if not matches_data:
            print("No matches found.")
            return

        conn = get_db_connection()
        if conn is None:
            print("Unable to connect to the database.")
            return
        
        inserted_count = 0
        skipped_count = 0

        #Loop through returned LLM matches, update matches table
        for match in matches_data:
            user_2_id = match.get("user_id")
            compatibility_score = match.get("compatibility_score")
            reasoning = match.get("reasoning")

            if not all([ref_user_id, compatibility_score, reasoning]):
                print(f"Skipping invalid match data: {match}")
                skipped_count += 1
                continue
        
            try:
                # Check if the match already exists and has a status of 'accepted'
                existing_match_response = conn.table("matches").select("status").or_(
                    f"(user_1_id.eq.{ref_user_id},user_2_id.eq.{user_2_id})",
                    f"(user_1_id.eq.{user_2_id},user_2_id.eq.{ref_user_id})"
                ).execute()

                existing_match_json = existing_match_response.get_json()
                status = existing_match_json.get("status")

                if existing_match_json and status == 'accepted':
                    print(f"Skipping update for match {ref_user_id} because it is already 'accepted'.")
                    skipped_count += 1
                    continue

                match_uuid = uuid.uuid4()

                #Make new match entry with returned data
                conn.table("matches").upsert({
                    "match_id": str(match_uuid),
                    "user_1_id": ref_user_id,
                    "user_2_id": user_2_id,
                    "match_score": compatibility_score,
                    "status": 'pending',
                    "reasoning": reasoning
                }).execute()
                inserted_count += 1
            except Exception as err:
                print(f"Database error for match {str(match_uuid)}: {err}")
                skipped_count += 1

    except Exception as err:
        print(f"Database error: {err}")

    except json.JSONDecodeError as err:
        print(f"JSON parsing error: {err}")