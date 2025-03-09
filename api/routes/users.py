from flask import Blueprint, Flask, jsonify, request, session
from flask_session import Session
from flask_cors import CORS
from api.database_connector import get_db_connection
from api.app import require_api_key
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
    finally:
        if conn:
            conn.close()

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
    finally:
        if conn:
            conn.close()


@user_routes.route("/api/users", methods=["POST"])
def add_user():
    conn = None
    try:
        data = request.json
        user_id = str(uuid.uuid4())
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500

        response = conn.table('users').insert({
            "user_id": user_id,
            "spotify_id": data["spotify_id"],
            "username": data["username"],
            "email": data["email"],
            "password_hash": data["password_hash"],
            "age": data["age"],
            "bio": data.get("bio", None)
        }).execute()

        if isinstance(response, dict) and "error" in response:
            raise Exception(response["error"]["message"])

        return jsonify({"message": "User added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()


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
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()


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
            "spotify_id": data["spotify_id"],
            "username": data["username"],
            "email": data["email"],
            "password_hash": data["password_hash"],
            "age": data["age"],
            "bio": data.get("bio", None)
        }).eq('user_id', str(user_uuid)).execute()

        if isinstance(response, dict) and "error" in response:
            raise Exception(response["error"]["message"])

        return jsonify({"message": "User updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()