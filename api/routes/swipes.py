from flask import Blueprint, Flask, jsonify, request, session
from flask_session import Session
from flask_cors import CORS
from database_connector import get_db_connection
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
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM swipes")
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(rows)
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    
@swipes_routes.route("/api/swipes/<swipe_id>", methods=["GET"])
def get_swipe(swipe_id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM swipes WHERE swipe_id = %s", (swipe_id,))
        rows = cursor.fetchone()

        cursor.close()
        conn.close()

        return jsonify(rows)
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500

@swipes_routes.route("/api/swipes", methods=["POST"])
def add_swipe():
    try:
        data = request.json
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500
        
        cursor = conn.cursor()

        query = """
        INSERT INTO swipes (swipe_id, swiper_id, swiped_id, action) 
        VALUES (UUID(), %s, %s, %s)
        """
        cursor.execute(query, (data["swiper_id"], data["swiped_id"], data["action"]))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Swipe recorded successfully"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    
@swipes_routes.route("/api/swipes/<swipe_id>", methods=["PUT"])
def update_swipe(swipe_id):
    try:
        data = request.json
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500
        
        cursor = conn.cursor()

        query = """
        UPDATE swipes 
        SET swiper_id = %s, swiped_id = %s, action = %s 
        WHERE swipe_id = %s
        """
        cursor.execute(query, (data["swiper_id"], data["swiped_id"], data["action"], swipe_id))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Match updated successfully"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500

@swipes_routes.route("/api/swipes/<swipe_id>", methods=["DELETE"])
def delete_swipe(swipe_id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500
        
        cursor = conn.cursor()

        cursor.execute("DELETE FROM swipes WHERE swipe_id = %s", (swipe_id,))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": "Swipe deleted successfully"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500