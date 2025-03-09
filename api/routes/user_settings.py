import uuid
from flask import Blueprint, Flask, jsonify, request, session
from flask_session import Session
from flask_cors import CORS
from database_connector import get_db_connection
import os
from dotenv import load_dotenv

user_setting_routes = Blueprint("user_setting_routes", __name__)

#API Key Authentication
API_ACCESS_KEY = os.getenv('API_ACCESS_KEY')

# -------------------- USER SETTINGS --------------------
@user_setting_routes.route("/api/user_settings", methods=["GET"])
def get_user_settings():
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_settings")
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(rows)
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    
@user_setting_routes.route("/api/user_settings/<user_setting_id>", methods=["GET"])
def get_user_setting(user_setting_id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500

        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE user_setting_id = %s", (user_setting_id,))
        rows = cursor.fetchone()

        cursor.close()
        conn.close()

        return jsonify(rows)
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    
@user_setting_routes.route("/api/user_settings", methods=["POST"])
def add_user_setting():
    try:
        data = request.json
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500
        
        cursor = conn.cursor()

        query = """
        INSERT INTO user_settings (setting_id, user_id, discoverability, notifications, theme_preference, language) 
        VALUES (UUID(), %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (data["user_id"], data["discoverability"], data["notifications"], data["theme_preference"], data["language"]))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "User settings added successfully"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500

@user_setting_routes.route("/api/user_settings/<user_id>", methods=["PUT"])
def update_user_settings(user_id):
    try:
        data = request.json
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500
        
        cursor = conn.cursor()

        query = """
        UPDATE user_settings 
        SET discoverability=%s, notifications=%s, theme_preference=%s, language=%s 
        WHERE user_id=%s
        """
        cursor.execute(query, (data["discoverability"], data["notifications"], data["theme_preference"], data["language"], user_id))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "User settings updated successfully"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    
@user_setting_routes.route("/api/user_settings/<user_setting_id>", methods=["DELETE"])
def delete_user_setting(user_setting_id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Unable to connect to the database"}), 500

        cursor = conn.cursor()

        query = """
        DELETE FROM user_settings 
        WHERE user_setting_id = %s
        """
        cursor.execute(query, (user_setting_id,))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "User settings deleted successfully"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500