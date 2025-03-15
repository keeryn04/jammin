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

@openai_routes.route("/api/chattesting/<ref_user_id>", methods=["GET"])
def run_ChatQuery(ref_user_id):
    messages = [
         {"role": "system", "content": 
          """You are a matchmaking compatibility score generator for music preferences. You will be given a list of users, each with their favorite songs, artists, and genres. 
          The first user in the list is the REFERENCE user. You will match them with all others and EXCLUDE them from the output. You Will prioritize top genres when giving a compatibility score, and be generous with scores.
          The output should be in JSON format and include the profile_name, common_top_songs, and common_top_artists of the matched user.
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
                "reasoning": "You share favorite artists and genres (provide example if they do), showing strong compatibility. your similar tastes suggest you would enjoy each other's playlists. Recommended artists: (provide recommendations based on both their top genres). (Keep reasoning ~30 words)",
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
        ref_user_data_id = get_user_data_id_by_user_id(ref_user_id)
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
            common_top_songs = find_common_elements(reference_user["top_songs"].split(", "), user["top_songs"].split(", "))
            common_top_artists = find_common_elements(reference_user["top_artists"].split(", "), user["top_artists"].split(", "))
 
            users_data.append({
                "user_data_id": user["user_data_id"],
                "profile_name": user["profile_name"],  # Include profile_name
                "topSongs": user["top_songs"],
                "topArtists": user["top_artists"],
                "topGenres": user["top_genres"],
                "common_top_songs": common_top_songs,  # Include common songs
                "common_top_artists": common_top_artists  # Include common artists
            })
        
        # Include the reference user in the data sent to the LLM
        users_data.insert(0, {
            "user_data_id": reference_user["user_data_id"],
            "profile_name": reference_user["profile_name"],  # Include profile_name
            "topSongs": reference_user["top_songs"],
            "topArtists": reference_user["top_artists"],
            "topGenres": reference_user["top_genres"]
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

        for match in matches_data:
            matched_user_id = get_user_id_by_user_data_id(match["user_data_id"])
            ref_user_id = get_user_id_by_user_data_id(ref_user_data_id)
            compatibility_score = match["compatibility_score"]
            reasoning = match["reasoning"]

            match_id = str(uuid.uuid4())

            # Check if a match already exists between these two users
            existing_match = conn.table("matches").select("match_id").eq("user_1_id", ref_user_id).eq("user_2_id", matched_user_id).execute()

            # If no match exists, insert the new match
            if not existing_match.data:
                data = {
                    "match_id": match_id,
                    "user_1_id": ref_user_id,
                    "user_2_id": matched_user_id,
                    "match_score": compatibility_score,
                    "status": "pending",
                    "reasoning": reasoning
                }

                # Insert into the table
                response = conn.table("matches").upsert(data, on_conflict=["match_id"]).execute()

                print(f"Response from upsert: {response}")  # Log full response object

                if response.data:  # Check if data was returned
                    print(f"Match inserted/updated for match_id {match_id}")
                else:
                    print(f"Failed to insert match for {matched_user_id} with match_id {match_id}.")
                    return jsonify({"error": f"Failed to insert or update match for {match_id}."}), 500
            else:
                print(f"Match already exists between {ref_user_id} and {matched_user_id}, skipping insertion.")

    except Exception as err:
        print(f"Database error: {err}")

    except json.JSONDecodeError as err:
        print(f"JSON parsing error: {err}")

def get_user_data_id_by_user_id(user_uuid):
    try:
        conn = get_db_connection()
        if conn is None:
            print("Connection Error")
            return None

        try:
            user_uuid = uuid.UUID(user_uuid)
        except ValueError:
            print("ID Error")
            return None  # Invalid format

        response = conn.table("users").select("user_data_id").eq('user_id', str(user_uuid)).execute()

        if not response.data:
            print("Connection Error")
            return None  # No user found

        return response.data[0]["user_data_id"]
    except Exception as err:
        return None

def get_user_id_by_user_data_id(user_data_uuid):
    try:
        conn = get_db_connection()
        if conn is None:
            print("Connection Error")
            return None

        try:
            user_data_uuid = uuid.UUID(user_data_uuid)
        except ValueError:
            print("ID Error")
            return None  # Invalid format

        response = conn.table("users").select("user_id").eq('user_data_id', str(user_data_uuid)).execute()

        if not response.data:
            print("No user found with the provided user_data_id")
            return None  # No user found

        return response.data[0]["user_id"]  # Return the user_id
    except Exception as err:
        return None
