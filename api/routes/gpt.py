from flask import Blueprint, app, jsonify, request, session, redirect, url_for
import os
from dotenv import load_dotenv
import uuid
import openai
import json

load_dotenv()
from database.database_connector import get_db_connection

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
               "reasoning": "You share favorite artists and genres (provide example if they do), showing strong compatibility. Your similar tastes suggest you would enjoy each other's playlists. Recommended artists: (provide recommendations based on both their top genres). (Keep reasoning ~30 words)",
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

        # Fetch the reference user
        response = conn.table("users_music_data").select("*").eq("user_data_id", ref_user_id).execute()
        reference_user = response.data[0] if response.data else None

        if not reference_user:
            return jsonify({"error": "Could not get your Profile."}), 404

        # Fetch all users excluding the reference user
        response = conn.table("users_music_data").select("*").neq("user_data_id", ref_user_id).execute()
        rows = response.data

        if not rows:
            return jsonify({"error": "No other users found for comparison"}), 404

        # Fetch ALL matches from the matches table
        matches_response = conn.table("matches").select("*").execute()
        matches_data = matches_response.data

        # Prepare the data for the LLM
        users_data = []
        for row in rows:
            # Check if a match exists for this user
            existing_match = next(
                (match for match in matches_data if match["user_1_data_id"] == ref_user_id and match["user_2_data_id"] == row["user_data_id"]),
                None
            )

            # Only include users with 'pending' status or no match
            if not existing_match or existing_match["status"] == "pending":
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
        print("LLM Raw Response:", reply)  # Log the raw LLM response

        # Parse the LLM's response
        try:
            parsed_reply = json.loads(reply)
            print("Parsed LLM Response:", parsed_reply)  # Log the parsed LLM response
        except json.JSONDecodeError as err:
            print("Failed to parse LLM response as JSON:", err)
            return jsonify({"error": "LLM response is not valid JSON"}), 500

        insert_response(parsed_reply, ref_user_id)

        return jsonify(parsed_reply)

    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


def insert_response(reply, ref_user_id):
    try:
        print("LLM Response (insert_response):", reply)  # Log the LLM's response
        matches_data = reply.get("matches", [])
        print(f"Number of matches returned by LLM: {len(matches_data)}")  # Log the number of matches

        if not matches_data:
            print("No matches found.")
            return

        conn = get_db_connection()
        if conn is None:
            print("Unable to connect to the database.")
            return

        inserted_count = 0
        skipped_count = 0

        for match in matches_data:
            user_id = match.get("userID")
            compatibility_score = match.get("compatibility_score")
            reasoning = match.get("reasoning")

            # Log the extracted data for debugging
            print(f"Extracted Match Data - userID: {user_id}, compatibility_score: {compatibility_score}, reasoning: {reasoning}")

            # Validate data
            if not user_id or not compatibility_score or not reasoning:
                print(f"Skipping invalid match data: {match}")
                skipped_count += 1
                continue

            # Log the data being inserted
            print(f"Inserting match: user_1_id={ref_user_id}, user_2_id={user_id}, match_score={compatibility_score}, reasoning={reasoning}")

            try:
                # Check if the match already exists and has a status of 'accepted'
                existing_match_response = conn.table("matches") \
                    .select("*") \
                    .filter("user_1_data_id", "eq", ref_user_id) \
                    .filter("user_2_data_id", "eq", user_id) \
                    .execute()

                existing_match_json = existing_match_response.data

                # If any match exists between these users, skip creating a new one
                if existing_match_json:
                    match_id = existing_match_json[0].get("match_id")
                    status = existing_match_json[0].get("status")
                    conn.table("matches").update({
                        "match_score": compatibility_score,
                        "reasoning": reasoning
                    }).filter("match_id", "eq", match_id).execute()
                    
                    print(f"Updating match {user_id} because it already exists. New Status: {status}.")
                    skipped_count += 1
                    continue

                match_uuid = uuid.uuid4()

                # Insert or update the match
                conn.table("matches").upsert({
                    "match_id": str(match_uuid),
                    "user_1_data_id": ref_user_id,
                    "user_2_data_id": user_id,
                    "match_score": compatibility_score,
                    "reasoning": reasoning,
                    "status": "pending"
                }).execute()
                inserted_count += 1
            except Exception as err:
                print(f"Database error for match {user_id}: {err}")
                skipped_count += 1

        print(f"Inserted {inserted_count} matches, skipped {skipped_count} matches.")

    except json.JSONDecodeError as err:
        print(f"JSON parsing error: {err}")
    except Exception as e:
        print(f"Unexpected error in insert_response: {str(e)}")