from flask import Blueprint, Flask, jsonify, request, session
from flask_session import Session
from flask_cors import CORS
from database_connector import get_db_connection
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
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM matches")
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(rows)
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    
@matches_routes.route("/api/matches/<match_id>", methods=["GET"])
def get_match(match_id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM matches WHERE match_id = %s", (match_id,))
        rows = cursor.fetchone()

        cursor.close()
        conn.close()

        return jsonify(rows)
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500

@matches_routes.route("/api/matches", methods=["POST"])
def add_match():
    try:
        data = request.json
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500
        
        cursor = conn.cursor()

        query = """
        INSERT INTO matches (match_id, user_1_id, user_2_id, match_score, status) 
        VALUES (UUID(), %s, %s, %s, %s)
        """
        cursor.execute(query, (data["user_1_id"], data["user_2_id"], data["match_score"], data["status"]))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Match added successfully"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    
@matches_routes.route("/api/matches/<match_id>", methods=["PUT"])
def update_match(match_id):
    try:
        data = request.json
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500
        
        cursor = conn.cursor()

        query = """
        UPDATE matches 
        SET user_1_id = %s, user_2_id = %s, match_score = %s, status = %s 
        WHERE match_id = %s
        """
        cursor.execute(query, (data["user_1_id"], data["user_2_id"], data["match_score"], data["status"], match_id))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Match updated successfully"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500


@matches_routes.route("/api/matches/<match_id>", methods=["DELETE"])
def delete_match(match_id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500
        
        cursor = conn.cursor()

        cursor.execute("DELETE FROM matches WHERE match_id = %s", (match_id,))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": "Match deleted successfully"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500