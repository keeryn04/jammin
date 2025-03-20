import uuid
from flask import Blueprint, Flask, jsonify, request, session
from database.database_connector import get_db_connection
import os
from dotenv import load_dotenv

user_data_routes = Blueprint("user_data_routes", __name__)

#API Key Authentication
API_ACCESS_KEY = os.getenv('API_ACCESS_KEY')

# -------------------- SPOTIFY DATA --------------------
@user_data_routes.route("/api/user_data", methods=["GET"])
def get_users_data():
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500

        response = conn.table("users_music_data").select("*").execute()

        if isinstance(response, dict) and "error" in response:
            raise Exception(response["error"]["message"])
        
        return jsonify(response.data), 200
    except Exception as err:
        return jsonify({"error": f"Database error: {err}"}), 500

@user_data_routes.route("/api/user_data", methods=["POST"])
def add_user_data():
    try:
        data = request.json
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500

        user_data_id = str(uuid.uuid4())

        response = conn.table("users_music_data").insert({
                "user_data_id": user_data_id,
                "user_id": data["user_id"],
                "spotify_id": data["spotify_id"],
                "top_songs": data["top_songs"],
                "top_songs_pictures": data["top_songs_pictures"],
                "top_artists": data["top_artists"],
                "top_artists_pictures": data["top_artists_pictures"],
                "top_genres": data["top_genres"],
                "top_genres_pictures": data["top_genres_pictures"],
                "profile_name": data["profile_name"],
                "profile_image": data["profile_image"]
        }).execute()

        if isinstance(response, dict) and "error" in response:
            raise Exception(response["error"]["message"])

        return jsonify({"message": "User data entry added successfully"}), 201
    except Exception as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    
@user_data_routes.route("/api/user_data/<user_data_id>", methods=["PUT"])
def update_user_data(user_data_id):
    conn = None
    try:
        data = request.json
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500
        
        try:
            user_data_uuid = uuid.UUID(user_data_id)
        except ValueError:
            return jsonify({"error": "Invalid user_data_id format"}), 400
        
        response = conn.table("users_music_data").insert({
                "spotify_id": data["spotify_id"],
                "top_songs": data["top_songs"],
                "top_songs_pictures": data["top_songs_pictures"],
                "top_artists": data["top_artists"],
                "top_artists_pictures": data["top_artists_pictures"],
                "top_genres": data["top_genres"],
                "top_genres_pictures": data["top_genres_pictures"],
                "profile_name": data["profile_name"],
                "profile_image": data["profile_image"]
        }).eq('user_data_id', str(user_data_uuid)).execute()

        if isinstance(response, dict) and "error" in response:
            raise Exception(response.error.message)

        return jsonify({"message": "User Settings updated successfully"}), 200
    except Exception as err:
        return jsonify({"error": f"Database error: {err}"}), 500

@user_data_routes.route("/api/user_data/<user_data_id>", methods=["DELETE"])
def delete_user_data(user_data_id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500
        
        try:
            user_data_uuid = uuid.UUID(user_data_id)
        except ValueError:
            return jsonify({"error": "Invalid user_data_id format"}), 400

        response = conn.table("users_music_data").delete().eq("user_data_id", str(user_data_uuid)).execute()

        if isinstance(response, dict) and "error" in response:
            raise Exception(response["error"]["message"])

        return jsonify({"message": "Music data deleted successfully"}), 200
    except Exception as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    
#For fetching data to send to ChatGPT
@user_data_routes.route("/api/user_data/<user_id>", methods=["GET"])
def get_user_music_data_by_id(user_id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500
        
        try:
            user_uuid = uuid.UUID(user_id)
        except ValueError:
            return jsonify({"error": "Invalid user_id format"}), 400

        row = conn.table("users_music_data").select("*").eq('user_id', str(user_uuid)).execute()

        if isinstance(response, dict) and "error" in response:
            raise Exception(response["error"]["message"])

        if row:
            response = {
                "user_id": row[0]["user_id"],
                "music_profile": {
                    "top_songs": row[0]["top_songs"],
                    "top_artists": row[0]["top_artists"],
                    "top_genres": row[0]["top_genres"]
                }
            }
        else:
            response = {"error": "User not found"}

        return jsonify(response.data), 200
    except Exception as err:
        return jsonify({"error": f"Database error: {err}"}), 500

#For fetching specific number of top artists  
@user_data_routes.route("/api/user_data/<user_id>/<int:limit>", methods=["GET"])
def get_user_top_artists_by_id(user_id, limit):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500

        row = conn.table("users_music_data").select("*").eq('user_id', user_id).execute()

        if isinstance(response, dict) and "error" in response:
            raise Exception(response["error"]["message"])

        if row:
            top_artists_list = row["top_artists"].split(", ")[:limit]
            top_artists_pictures_list = row["top_artists_pictures"].split(", ")[:limit]
            response = {
                "user_id": user_id,
                "top_artists": top_artists_list,
                "top_artists_pictures": top_artists_pictures_list
            }
        else:
            response = {"error": "User not found"}

        return jsonify(response.data), 200
    except Exception as err:
        return jsonify({"error": f"Database error: {err}"}), 500