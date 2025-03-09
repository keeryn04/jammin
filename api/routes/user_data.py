import uuid
from flask import Blueprint, Flask, jsonify, request, session
from flask_session import Session
from flask_cors import CORS
from api.database_connector import get_db_connection
from api.app import require_api_key
import os
from dotenv import load_dotenv

user_data_routes = Blueprint("user_data_routes", __name__)

#API Key Authentication
API_ACCESS_KEY = os.getenv('API_ACCESS_KEY')

# -------------------- SPOTIFY DATA --------------------
@user_data_routes.route("/api/user_data", methods=["GET"])
def get_user_data():
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
    
#For fetching data to send to ChatGPT
@user_data_routes.route("/api/user_data/<user_id>", methods=["GET"])
def get_user_data_by_user_id(user_id):
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

@user_data_routes.route("/api/user_data", methods=["POST"])
def add_user_data():
    try:
        data = request.json
        user_data_id = str(uuid.uuid4())
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO users_music_data (user_data_id, user_id, top_songs, top_songs_pictures, 
                                      top_artists, top_artists_pictures, top_genres, top_genres_pictures, 
                                      profile_name, profile_image) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            user_data_id, data["user_id"], data["top_songs"], data["top_songs_pictures"],
            data["top_artists"], data["top_artists_pictures"], data["top_genres"], data["top_genres_pictures"],
            data["profile_name"], data["profile_image"]
        ))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Music entry added successfully"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500

@user_data_routes.route("/api/user_data/<user_id>", methods=["DELETE"])
def delete_user_data(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users_music_data WHERE user_id = %s", (user_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Music data deleted successfully"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500

@user_data_routes.route("/api/user_data/<user_id>", methods=["PUT"])
def update_user_data(user_id):
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        UPDATE users_music_data 
        SET top_songs=%s, top_songs_pictures=%s, 
            top_artists=%s, top_artists_pictures=%s, 
            top_genres=%s, top_genres_pictures=%s, 
            profile_name=%s, profile_image=%s 
        WHERE user_id=%s
        """
        cursor.execute(query, (
            data.get("top_songs"), data.get("top_songs_pictures"),
            data.get("top_artists"), data.get("top_artists_pictures"),
            data.get("top_genres"), data.get("top_genres_pictures"),
            data.get("profile_name"), data.get("profile_image"), user_id
        ))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Music data updated successfully"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500