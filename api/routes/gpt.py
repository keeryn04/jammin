from flask import Blueprint, app, jsonify, request
from flask_cors import CORS
import os
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
        
        #Fetch the reference user
        response = conn.table("users_music_data").select("*").eq("user_data_id", ref_user_data_id).execute()

        if not response.data:
            return jsonify({"error": "Could not get your Profile."}), 404
        
        reference_user = response.data[0]

        #Fetch all users excluding the reference user
        response = conn.table("users_music_data").select("*").neq("user_data_id", ref_user_data_id).execute()
        other_users = response.data

        if not other_users:
            return jsonify({"error": "No other users found for comparison"}), 404

        #Fetch all matches from the matches table
        matches_response = conn.table("matches").select("*").execute()
        matches_data = matches_response.data

        other_user_data_id = user["user_data_id"]

        #Prepare the data for the LLM
        users_data = []
        for user in other_users:
            #Check if a match exists for this user
            existing_match = next(
                (match for match in matches_data if 
                    ((match.get("user_1_data_id") == ref_user_data_id and match.get("user_2_data_id") == other_user_data_id) or
                    (match.get("user_1_data_id") == other_user_data_id and match.get("user_2_data_id") == ref_user_data_id))),
                None
            )

            #Only include users with 'pending' status or no match
            if not existing_match or existing_match["status"] == "pending":
                users_data.append({
                    "user_data_id": reference_user["user_data_id"],
                    "profile_name": reference_user["profile_name"],
                    "topSongs": reference_user["top_songs"].split(", "),
                    "topArtists": reference_user["top_artists"].split(", "),
                    "topGenres": reference_user["top_genres"].split(", ")
                })

        #Include the reference user in the data sent to the LLM
        users_data.insert(0, {
            "user_data_id": reference_user["user_data_id"],
            "profile_name": reference_user["profile_name"],
            "topSongs": reference_user["top_songs"].split(", "),
            "topArtists": reference_user["top_artists"].split(", "),
            "topGenres": reference_user["top_genres"].split(", ")
        })

        #Create LLM content
        message_content = json.dumps(users_data)
        messages.append({"role": "user", "content": message_content})

        #Call the LLM
        chat = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            response_format={"type": "json_object"}
        )

        #Parse reply, and insert into database
        reply = chat.choices[0].message.content
        insert_response(reply, ref_user_data_id)

        return jsonify(json.loads(reply))

    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


def insert_response(reply, ref_user_data_id):
    try:
        #Parse matches from reply
        matches_data = reply.get("matches", [])

        if not matches_data:
            print("No matches found.")
            return

        conn = get_db_connection()
        if conn is None:
            print("Unable to connect to the database.")
            return

        inserted_count = 0
        skipped_count = 0

        #Check if match already exists, and is valid, add otherwise
        for match in matches_data:
            #Get other user's data
            user_2_data_id = match.get("userID")
            compatibility_score = match.get("compatibility_score")
            reasoning = match.get("reasoning")

            #Invalid match catch
            if not all([user_2_data_id, compatibility_score, reasoning]):
                print(f"Skipping invalid match data: {match}")
                skipped_count += 1
                continue

            try:
                #Check for existing matches from matches table
                existing_match_response = conn.table("matches").select("status").or_(
                    f"(user_1_data_id.eq.{ref_user_data_id},user_2_data_id.eq.{user_2_data_id})",
                    f"(user_1_data_id.eq.{user_2_data_id},user_2_data_id.eq.{ref_user_data_id})"
                ).execute()

                existing_match_json = existing_match_response.get_json()
                status = existing_match_json.get("status")

                #Make sure match isn't already 'accepted'
                if existing_match_json and status == 'accepted':
                    print(f"Skipping update for match {ref_user_data_id} because it is already 'accepted'.")
                    skipped_count += 1
                    continue

                #Make new uuid for match
                match_uuid = uuid.uuid4()

                #Insert or update the match
                conn.table("matches").upsert({
                    "match_id": str(match_uuid),
                    "user_1_data_id": ref_user_data_id,
                    "user_2_data_id": user_2_data_id,
                    "match_score": compatibility_score,
                    "status": 'pending',
                    "reasoning": reasoning
                }).execute()
                inserted_count += 1
            except Exception as err:
                print(f"Database error for match {match_uuid}: {err}")
                skipped_count += 1

    except json.JSONDecodeError as err:
        print(f"JSON parsing error: {err}")
    except Exception as e:
        print(f"Unexpected error in insert_response: {str(e)}")