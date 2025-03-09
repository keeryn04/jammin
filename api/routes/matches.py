from flask import Blueprint, Flask, jsonify, request, session
from flask_session import Session
from flask_cors import CORS
from api.database_connector import get_db_connection
from api.app import require_api_key
import os
import uuid
from dotenv import load_dotenv

matches_routes = Blueprint("matches_routes", __name__)

#API Key Authentication
API_ACCESS_KEY = os.getenv('API_ACCESS_KEY')

# -------------------- MATCHES --------------------
@matches_routes.route("/api/matches", methods=["GET"])
def get_matches():
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500

        response = conn.table("matches").select("*").execute()
        
        if isinstance(response, dict) and "error" in response:
            raise Exception(response["error"]["message"])

        return jsonify(response.data), 200
    except Exception as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    
@matches_routes.route("/api/matches/<match_id>", methods=["GET"])
def get_match(match_id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500
        
        try:
            match_uuid = uuid.UUID(match_id)
        except ValueError:
            return jsonify({"error": "Invalid match_id format"}), 400
        
        response = conn.table("matches").select("*").eq('match_id', str(match_uuid)).execute()

        if isinstance(response, dict) and "error" in response:
            raise Exception(response["error"]["message"])

        return jsonify(response.data), 200
    except Exception as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    finally:
        if conn:
            conn.close()

@matches_routes.route("/api/matches/<match_id>", methods=["POST"])
def add_match(match_id):
    try:
        data = request.json
        match_id = str(uuid.uuid4())
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500

        response = conn.table("matches").update({
            "match_id": match_id,
            "user_1_id": data["user_1_id"],
            "user_2_id": data["user_2_id"],
            "match_score": data["match_score"],
            "status": data["status"]
        }).execute()

        if isinstance(response, dict) and "error" in response:
            raise Exception(response["error"]["message"])

        return jsonify({"message": "Match added successfully"}), 200
    except Exception as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    finally:
        if conn:
            conn.close()

@matches_routes.route("/api/matches/<match_id>", methods=["DELETE"])
def delete_match(match_id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500
        
        try:
            match_uuid = uuid.UUID(match_id)
        except ValueError:
            return jsonify({"error": "Invalid match_id format"}), 400

        response = conn.table('matches').delete().eq('match_id', str(match_uuid)).execute()
        
        if isinstance(response, dict) and "error" in response:
            raise Exception(response["error"]["message"])

        return jsonify({"message": "Match deleted successfully"}), 200
    except Exception as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    finally:
        if conn:
            conn.close()