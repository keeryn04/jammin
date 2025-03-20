from flask import Blueprint, Flask, jsonify, make_response, request, session
from flask_session import Session
from flask_cors import CORS
from database.database_connector import get_db_connection
import os
import uuid

from api.jwt import generate_jwt
from api.auth_helpers import hash_password

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

        hashed_password = hash_password(data["password_hash"])

        response = conn.table('users').insert({
            "user_id": user_uuid,
            "user_data_id": user_data_uuid,
            "username": data["username"],
            "email": data["email"],
            "password_hash": hashed_password,
            "age": data["age"],
            "gender": data["gender"], 
            "spotify_auth": data["spotify_auth"],
            "bio": data.get("bio", None)
        }).execute()

        response = conn.table('users_music_data').insert({
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

        jwt_token = generate_jwt(user_uuid, user_data_uuid) #Store current user_id and user_data_id as cookie (Register)
        
        response = make_response(jsonify({"message": "Register successful", "user_id": user_uuid}))
        response.set_cookie("auth_token", jwt_token, httponly=True, secure=True, samesite="None", max_age=3600)
    
        if isinstance(response, dict) and "error" in response:
            raise Exception(response["error"]["message"])

        return response, 201
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

        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    
@user_routes.route("/api/users/by_user_data/<user_data_id>", methods=["GET"])
def get_user_id_by_user_data_id(user_data_id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Connection Error"}), 500

        try:
            user_data_uuid = uuid.UUID(user_data_id)
        except ValueError:
            return jsonify({"error": "ID Error"}), 400  # Invalid format

        response = conn.table("users").select("user_id").eq('user_data_id', str(user_data_uuid)).execute()

        if not response.data:
            return jsonify({"error": "No user found with the provided user_data_id"}), 404

        return jsonify({"user_id": response.data[0]["user_id"]})
    except Exception as err:
        return jsonify({"error": str(err)}), 500
    
@user_routes.route("/api/user_data/by_user/<user_id>", methods=["GET"])
def get_user_data_id_by_user_id(user_id):
    try:
        conn = get_db_connection()
        if conn is None:
            print("Connection Error")
            return None

        try:
            user_uuid = uuid.UUID(user_id)
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
