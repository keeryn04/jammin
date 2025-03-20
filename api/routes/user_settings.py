import uuid
from flask import Blueprint, Flask, jsonify, request, session
from flask_session import Session
from flask_cors import CORS
from database.database_connector import get_db_connection
import mysql.connector
import os
from dotenv import load_dotenv

user_setting_routes = Blueprint("user_setting_routes", __name__)

#API Key Authentication
API_ACCESS_KEY = os.getenv('API_ACCESS_KEY')

# -------------------- USER SETTINGS --------------------
@user_setting_routes.route("/api/user_settings", methods=["GET"])
def get_user_settings():
    conn = None
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500

        response = conn.table("user_settings").select("*").execute()
        
        if isinstance(response, dict) and "error" in response:
            raise Exception(response["error"]["message"])

        return jsonify(response.data), 200
    except Exception as err:
        return jsonify({"error": f"Database error: {err}"}), 500

@user_setting_routes.route("/api/user_settings/<setting_id>", methods=["GET"])
def get_user_setting(setting_id):
    conn = None
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500
        
        try:
            setting_uuid = uuid.UUID(setting_id)
        except ValueError:
            return jsonify({"error": "Invalid setting_id format"}), 400

        response = conn.table("user_settings").select("*").eq('setting_id', str(setting_uuid)).execute()
        
        if isinstance(response, dict) and "error" in response:
            raise Exception(response["error"]["message"])

        return jsonify(response.data), 200
    except Exception as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    
@user_setting_routes.route("/api/user_settings", methods=["POST"])
def add_user_settings():
    conn = None
    try:
        data = request.json
        setting_id = str(uuid.uuid4())
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500

        response = conn.table('user_settings').insert({
            "setting_id": setting_id,
            "user_id": data["user_id"],
            "discoverability": data.get("discoverability", True),
            "notifications": data.get("notifications", True),
            "theme_preference": data.get("theme_preference", "light"),
            "language": data.get("language", "en"),
        }).execute()

        if isinstance(response, dict) and "error" in response:
            raise Exception(response["error"]["message"])

        return jsonify({"message": "User settings added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_setting_routes.route("/api/user_settings/<setting_id>", methods=["PUT"])
def update_user_settings(setting_id):
    conn = None
    try:
        data = request.json
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500
        
        try:
            setting_uuid = uuid.UUID(setting_id)
        except ValueError:
            return jsonify({"error": "Invalid setting_id format"}), 400
        
        response = conn.table('user_settings').update({
            "user_id": data["user_id"],
            "discoverability": data["discoverability"],
            "notifications": data["notifications"],
            "theme_preference": data["theme_preference"],
            "language": data["language"]
        }).eq('setting_id', str(setting_uuid)).execute()

        if isinstance(response, dict) and "error" in response:
            raise Exception(response.error.message)

        return jsonify({"message": "User Settings updated successfully"}), 200
    except Exception as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    
@user_setting_routes.route("/api/user_settings/<setting_id>", methods=["DELETE"])
def delete_user_settings(setting_id):
    conn = None
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500
        
        try:
            setting_uuid = uuid.UUID(setting_id)
        except ValueError:
            return jsonify({"error": "Invalid setting_id format"}), 400

        response = conn.table('user_settings').delete().eq('setting_id', str(setting_uuid)).execute()

        if isinstance(response, dict) and "error" in response:
            raise Exception(response["error"]["message"])

        return jsonify({"message": "Settings deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
