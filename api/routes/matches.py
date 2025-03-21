from flask import Blueprint, jsonify, request, session
from database.database_connector import get_db_connection
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

@matches_routes.route("/api/matches", methods=["POST"])
def add_match():
    try:
        data = request.json
        match_id = str(uuid.uuid4())
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500

        response = conn.table("matches").upsert({
            "match_id": match_id,
            "user_1_data_id": data["user_1_data_id"],
            "user_2_data_id": data["user_2_data_id"],
            "match_score": data["match_score"],
            "status": data["status"],
            "reasoning":data["reasoning"]
        }).execute()

        if isinstance(response, dict) and "error" in response:
            raise Exception(response["error"]["message"])

        return jsonify({"message": "Match added successfully"}), 200
    except Exception as err:
        return jsonify({"error": f"Database error: {err}"}), 500

@matches_routes.route("/api/matches/<match_id>", methods=["PUT"])
def update_match(match_id):
    print(f"Received PUT request for match_id: {match_id}")
    conn = None
    try:
        data = request.json
        print(f"Request data: {data}")

        if not data:
            print("Error: Request JSON data is empty or None")
            return jsonify({"error": "Invalid JSON data"}), 400
    
        conn = get_db_connection()
        if conn is None:
            print("Error: Unable to connect to the database")
            return jsonify({"error": "Unable to connect to the database"}), 500
        
        try:
            match_uuid = uuid.UUID(match_id)
            print(f"Validated match_id: {match_uuid}")
        except ValueError:
            print(f"Error: Invalid match_id format: {match_id}")
            return jsonify({"error": "Invalid match_id format"}), 400
        
        print("Updating match in database...")
        response = conn.table("matches").update({
            "user_1_data_id": data["user_1_id"],
            "user_2_data_id": data["user_2_id"],
            "match_score": data["match_score"],
            "status": data["status"],
            "reasoning": data["reasoning"]
        }).eq('match_id', str(match_uuid)).execute()

        print(f"Database response: {response}")

        if isinstance(response, dict) and "error" in response:
            print(f"Database error: {response['error']['message']}")  # Debug log
            raise Exception(response["error"]["message"])

        print("Match updated successfully.")
        return jsonify({"message": "Match updated successfully"}), 200
    except Exception as err:
        print("Unexpected error occurred!")  # Debug log
        return jsonify({"error": f"Database error: {err}"}), 500

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