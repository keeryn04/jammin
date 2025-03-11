from flask import Blueprint, Flask, jsonify, request, session
from flask_session import Session
from flask_cors import CORS
from api.database_connector import get_db_connection
import os
import uuid

user_routes = Blueprint("user_routes", __name__)

#API Key Authentication
API_ACCESS_KEY = os.getenv('API_ACCESS_KEY')

# -------------------- USERS --------------------
@user_routes.route("/api/users", methods=["GET"])
def get_users():
    conn = None
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500

        response = conn.table("users").select("*").execute()

        if isinstance(response, dict) and "error" in response:
            raise Exception(response["error"]["message"])

        return jsonify(response.data), 200
    except Exception as err:
        return jsonify({"error": f"Database error: {err}"}), 500

@user_routes.route("/api/users/<user_id>", methods=["GET"])
def get_user(user_id):
    conn = None
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500
        
        try:
            user_uuid = uuid.UUID(user_id)
        except ValueError:
            return jsonify({"error": "Invalid user_id format"}), 400

        response = conn.table("users").select("*").eq('user_id', str(user_uuid)).execute()

        if isinstance(response, dict) and "error" in response:
            raise Exception(response["error"]["message"])

        return jsonify(response.data), 200
    except Exception as err:
        return jsonify({"error": f"Database error: {err}"}), 500

@user_routes.route("/api/users", methods=["POST"])
def add_user():
    conn = None
    try:
        data = request.json
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500

        user_uuid = str(uuid.uuid4())
        user_data_uuid = str(uuid.uuid4())

        response = conn.table('user_music_data').insert({
            "user_data_id": user_data_uuid,
            "profile_name": "",
            "profile_image": "",
            "top_songs": "",
            "top_songs_pictures": "",
            "top_artists": "",
            "top_artists_pictures": "",
            "top_genres": "",
            "top_genres_pictures": ""
        }).execute()

        response = conn.table('users').insert({
            "user_id": user_uuid,
            "user_data_id": user_data_uuid,
            "username": data["username"],
            "email": data["email"],
            "password_hash": data["password_hash"],
            "age": data["age"],
            "gender": data["gender"], 
            "spotify_auth": data["spotify_auth"],
            "bio": data.get("bio", None)
        }).execute()

        session["current_user_id"] = user_uuid #Store current user_id as session variable (Register)

        if isinstance(response, dict) and "error" in response:
            raise Exception(response["error"]["message"])

        return jsonify({"message": "User added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_routes.route("/api/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    conn = None
    try:
        data = request.json
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500
        
        try:
            user_uuid = uuid.UUID(user_id)
        except ValueError:
            return jsonify({"error": "Invalid user_id format"}), 400
        
        response = conn.table('users').update({
            "username": data["username"],
            "email": data["email"],
            "password_hash": data["password_hash"],
            "age": data["age"],
            "gender": data.get("gender"), 
            "school": data.get("school"), 
            "occupation": data.get("occupation"), 
            "looking_for": data.get("looking_for"), 
            "spotify_auth": data.get("spotify_auth", False), #Default to False
            "bio": data.get("bio", None)
        }).eq('user_id', str(user_uuid)).execute()

        if isinstance(response, dict) and "error" in response:
            raise Exception(response.error.message)

        return jsonify({"message": "User updated successfully"}), 201
    except Exception as err:
        return jsonify({"error": f"Database error: {err}"}), 500

@user_routes.route("/api/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    conn = None
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500

        try:
            user_uuid = uuid.UUID(user_id)
        except ValueError:
            return jsonify({"error": "Invalid user_id format"}), 400

        response = conn.table('users').delete().eq('user_id', str(user_uuid)).execute()

        if isinstance(response, dict) and "error" in response:
            raise Exception(response["error"]["message"])

        return jsonify({"message": "User deleted successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500