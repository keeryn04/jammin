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
         {'user_data_id':'0', 'profile_name': 'Tony Stark', 'topSongs':['SongA', 'SongB'], 'topArtists':['ArtistA', 'ArtistB'], 'topGenres':['GenreA']},
         {'user_data_id':'72', 'profile_name': 'Thor', 'topSongs':['SongB', 'SongC'], 'topArtists':['ArtistB', 'ArtistC'], 'topGenres':['GenreB']}
         ]
         Example output:
         {
           "matches": [
             {
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

        # Grab first user as reference user
        response = conn.table("users_music_data").select("*").eq("user_data_id", ref_user_data_id).execute()

        if not response.data:
            return jsonify({"error": "Could not get your Profile."}), 404
        
        reference_user = response.data[0]

        print("Returned Reference User:", reference_user)

        rows = conn.table("users_music_data").select("*").neq("user_data_id", ref_user_data_id).execute()

        if not rows:
             return jsonify({"error": "No other users found for comparison"}), 404
        
        other_users = rows.data
        print("Other Users:", other_users)

        users_data = []
        for user in other_users:
            users_data.append({
                "user_data_id": user["user_data_id"],
                "profile_name": user["profile_name"],
                "topSongs": user["top_songs"].split(", "),
                "topArtists": user["top_artists"].split(", "),
                "topGenres": user["top_genres"].split(", ")
            })
        
        # Include the reference user in the data sent to the LLM
        users_data.insert(0, {
            "user_data_id": reference_user["user_data_id"],
            "profile_name": reference_user["profile_name"],
            "profile_name": reference_user["profile_name"],
             "topSongs": reference_user["top_songs"].split(", "),
             "topArtists": reference_user["top_artists"].split(", "),
             "topGenres": reference_user["top_genres"].split(", ")
        })

        print("Users Data Sent to LLM:", users_data)

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

        insert_response(reply, ref_user_data_id)

        return jsonify(json.loads(reply))

    except Exception as err:
        return jsonify({"error": f"Database error: {err}"}), 500

    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

def insert_response(reply, ref_user_data_id):
    try:
        matches_data = json.loads(reply).get("matches", [])

        if not matches_data:
            print("No matches found.")
            return

        conn = get_db_connection()
        if conn is None:
            print("Unable to connect to the database.")
            return

        #Fetch user IDs for all matches in one query
        user_data_ids = [match["user_data_id"] for match in matches_data]
        user_data_ids.append(ref_user_data_id)  #Include reference user

        response = conn.table("users").select("user_id", "user_data_id").in_("user_data_id", user_data_ids).execute()
        user_id_map = {row["user_data_id"]: row["user_id"] for row in response.data}

        ref_user_id = user_id_map.get(ref_user_data_id)
        if not ref_user_id:
            print("Reference user ID not found.")
            return

        #Fetch all existing matches in one query
        match_ids = conn.table("matches").select("match_id", "user_1_id", "user_2_id").or_(
            f"user_1_id.eq.{ref_user_id}, user_2_id.eq.{ref_user_id}"
        ).execute()

        existing_matches = {(row["user_1_id"], row["user_2_id"]): row["match_id"] for row in match_ids.data}

        upsert_data = []
        for match in matches_data:
            matched_user_id = user_id_map.get(match["user_data_id"])
            if not matched_user_id:
                continue  #Skip if no user ID found

            compatibility_score = match["compatibility_score"]
            reasoning = match["reasoning"]

            #Check if a match already exists
            existing_match_id = existing_matches.get((ref_user_id, matched_user_id)) or existing_matches.get((matched_user_id, ref_user_id))

            if existing_match_id: # Update existing match
                upsert_data.append({
                    "match_id": existing_match_id,
                    "match_score": compatibility_score,
                    "reasoning": reasoning
                })
            else: #Insert new match
                upsert_data.append({
                    "match_id": str(uuid.uuid4()),
                    "user_1_id": ref_user_id,
                    "user_2_id": matched_user_id,
                    "match_score": compatibility_score,
                    "status": "pending",
                    "reasoning": reasoning
                })

        if upsert_data:
            #Perform batch upsert
            response = conn.table("matches").upsert(upsert_data, on_conflict=["match_id"]).execute()
            print(f"Upsert response: {response}")

    except Exception as err:
        print(f"Database error: {err}")

    except json.JSONDecodeError as err:
        print(f"JSON parsing error: {err}")
