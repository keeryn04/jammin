import uuid
from flask import Blueprint, jsonify, request, session
from database.database_connector import get_db_connection
import os

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