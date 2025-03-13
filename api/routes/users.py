from flask import Blueprint, Flask, jsonify, request, session
from flask_session import Session
from flask_cors import CORS
from database_connector import get_db_connection
import mysql.connector
import os
import uuid

user_routes = Blueprint("user_routes", __name__)

#API Key Authentication
API_ACCESS_KEY = os.getenv('API_ACCESS_KEY')

# -------------------- USERS --------------------
@user_routes.route("/api/users", methods=["GET"])
def get_users():
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(rows)
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500

@user_routes.route("/api/users/<user_id>", methods=["GET"])
def get_user(user_id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500

        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        rows = cursor.fetchone()

        cursor.close()
        conn.close()

        return jsonify(rows)
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500

@user_routes.route("/api/users", methods=["POST"])
def add_user():
    try:
        data = request.json
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500

        cursor = conn.cursor()

        user_id = str(uuid.uuid4())
        user_data_uuid = str(uuid.uuid4())

        query_user_data = """
        INSERT INTO users_music_data (user_data_id, spotify_id, profile_name, profile_image, 
        top_songs, top_songs_pictures, top_artists, top_artists_pictures, top_genres, top_genres_pictures) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
        """

        cursor.execute(query_user_data, (user_data_uuid, "", "", "", "", "", "", "", "", ""))

        query_users = """
        INSERT INTO users (user_id, user_data_id, username, email, password_hash, age, gender, spotify_auth, bio) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) 
        """

        cursor.execute(query_users, (user_id, user_data_uuid, data["username"], data["email"], data["password_hash"], data["age"], data["gender"], data["spotify_auth"], data.get("bio")))

        #Store current user_id as session variable (Register)
        session["current_user_id"] = user_id

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "User added successfully"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    
@user_routes.route("/api/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    try:
        data = request.json
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500
            
        cursor = conn.cursor()

        query = """
        UPDATE users 
        SET username=%s, email=%s, password_hash=%s, age=%s, bio=%s, 
            gender=%s, school=%s, occupation=%s, looking_for=%s, spotify_auth=%s
        WHERE user_id=%s
        """
        cursor.execute(query, (
            data["username"], data["email"], data["password_hash"], data["age"], data.get("bio"),
            data.get("gender"), data.get("school"), data.get("occupation"), data.get("looking_for"), 
            data.get("spotify_auth", False),  #Default to False
            user_id
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "User updated successfully"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500

@user_routes.route("/api/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500

        cursor = conn.cursor()

        cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": "User deleted successfully"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    
@user_routes.route("/api/users/by_user_data/<user_data_id>", methods=["GET"])
def get_user_by_user_data(user_data_id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500

        cursor = conn.cursor(dictionary=True)
        
        # Fetch user_id from the users table using user_data_id
        cursor.execute("SELECT * FROM users WHERE user_data_id = %s", (user_data_id,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            return jsonify(user)
        else:
            return jsonify({"error": "User not found"}), 404
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500
