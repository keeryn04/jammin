import uuid
from flask import Blueprint, Flask, jsonify, request, session
from flask_session import Session
from flask_cors import CORS
from database_connector import get_db_connection
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
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users_music_data")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(rows)
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500

@user_data_routes.route("/api/user_data", methods=["POST"])
def add_user_data():
    try:
        data = request.json
        user_data_id = str(uuid.uuid4())
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500
        
        cursor = conn.cursor()

        query = """
        INSERT INTO users_music_data (user_data_id, spotify_id, top_songs, top_songs_pictures, 
                                      top_artists, top_artists_pictures, top_genres, top_genres_pictures, 
                                      profile_name, profile_image) 
        VALUES (UUID(), %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            user_data_id, data["spotify_id"], data["top_songs"], data["top_songs_pictures"],
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
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500
        
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users_music_data WHERE user_id = %s", (user_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Music data deleted successfully"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500

@user_data_routes.route("/api/user_data/<user_data_id>", methods=["PUT"])
def update_user_data(user_data_id):
    try:
        data = request.json
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500

        cursor = conn.cursor()

        query = """
        UPDATE users_music_data 
        SET top_songs=%s, top_songs_pictures=%s, 
            top_artists=%s, top_artists_pictures=%s, 
            top_genres=%s, top_genres_pictures=%s, 
            profile_name=%s, profile_image=%s 
        WHERE user_data_id=%s
        """
        cursor.execute(query, (
            data.get("top_songs"), data.get("top_songs_pictures"),
            data.get("top_artists"), data.get("top_artists_pictures"),
            data.get("top_genres"), data.get("top_genres_pictures"),
            data.get("profile_name"), data.get("profile_image"), user_data_id
        ))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Music data updated successfully"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    
#For fetching data to send to ChatGPT
@user_data_routes.route("/api/user_data/<user_id>", methods=["GET"])
def get_user_music_data_by_id(user_id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT user_data_id FROM users WHERE user_id = %s", (user_id,))
        user_data_id = cursor.fetchone()

        cursor.execute("SELECT * FROM users_music_data WHERE user_data_id = %s", (user_data_id,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        if rows:
            response = {
                "user_id": rows[0]["user_id"],
                "music_profile": {
                    "top_songs": rows[0]["top_songs"],
                    "top_artists": rows[0]["top_artists"],
                    "top_genres": rows[0]["top_genres"]
                }
            }
        else:
            response = {"error": "User not found"}

        return jsonify(response)
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500

#For fetching specific number of top artists  
@user_data_routes.route("/api/user_data/<user_id>/<int:limit>", methods=["GET"])
def get_user_top_artists_by_id(user_id, limit):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT user_data_id FROM users WHERE user_id = %s", (user_id,))
        user_data_id = cursor.fetchone()

        cursor.execute("SELECT * FROM users_music_data WHERE user_data_id = %s", (user_data_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
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

        return jsonify(response)
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500