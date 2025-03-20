from flask import Blueprint, Flask, jsonify, request, session
from flask_session import Session
from flask_cors import CORS
from database.database_connector import get_db_connection
import mysql.connector
import os
import uuid
from dotenv import load_dotenv

swipes_routes = Blueprint("swipes_routes", __name__)

#API Key Authentication
API_ACCESS_KEY = os.getenv('API_ACCESS_KEY')

# -------------------- SWIPES --------------------
@swipes_routes.route("/api/swipes", methods=["GET"])
def get_swipes():
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500
        
        response = conn.table("swipes").select("*").execute()

        if isinstance(response, dict) and "error" in response:
            raise Exception(response["error"]["message"])

        return jsonify(response.data), 200
    except Exception as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    
@swipes_routes.route("/api/swipes/<swipe_id>", methods=["GET"])
def get_swipe(swipe_id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500
        
        try:
            swipe_uuid = uuid.UUID(swipe_id)
        except ValueError:
            return jsonify({"error": "Invalid user_id format"}), 400
        
        response = conn.table("swipes").select("*").eq('swipe_id', str(swipe_uuid)).execute()

        if isinstance(response, dict) and "error" in response:
            raise Exception(response["error"]["message"])

        return jsonify(response.data), 200
    except Exception as err:
        return jsonify({"error": f"Database error: {err}"}), 500

@swipes_routes.route("/api/swipes", methods=["POST"])
def add_swipe(swipe_id):
    try:
        data = request.json
        swipe_id = str(uuid.uuid4())
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500

        response = conn.table("swipes").upsert({
            "swipe_id": swipe_id,
            "swiper_id": data["swiper_id"],
            "swiped_id": data["swiped_id"],
            "action": data["action"]
        }).execute()

        if isinstance(response, dict) and "error" in response:
            raise Exception(response["error"]["message"])

        return jsonify({"message": "Swipe recorded successfully"}), 200
    except Exception as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    
@swipes_routes.route("/api/swipes/<swipe_id>", methods=["POST"])
def update_swipe(swipe_id):
    conn = None
    try:
        data = request.json
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500
        
        try:
            swipe_uuid = uuid.UUID(swipe_id)
        except ValueError:
            return jsonify({"error": "Invalid swipe_id format"}), 400
        
        response = conn.table("swipes").update({
            "swiper_id": data["swiper_id"],
            "swiped_id": data["swiped_id"],
            "action": data["action"]
        }).eq('swipe_id', str(swipe_uuid)).execute()

        if isinstance(response, dict) and "error" in response:
            raise Exception(response.error.message)

        return jsonify({"message": "Swipe updated successfully"}), 200
    except Exception as err:
        return jsonify({"error": f"Database error: {err}"}), 500

@swipes_routes.route("/api/swipes/<swipe_id>", methods=["DELETE"])
def delete_swipe(swipe_id):
    conn = None
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500

        try:
            swipe_uuid = uuid.UUID(swipe_id)
        except ValueError:
            return jsonify({"error": "Invalid swipe_id format"}), 400

        response = conn.table('user_settings').delete().eq('setting_id', str(swipe_uuid)).execute()

        if isinstance(response, dict) and "error" in response:
            raise Exception(response["error"]["message"])

        return jsonify({"message": "Swipe deleted successfully"}), 200
    except Exception as err:
        return jsonify({"error": f"Database error: {err}"}), 500