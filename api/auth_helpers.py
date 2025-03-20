import bcrypt
from flask import Blueprint, json, jsonify, request

from api.jwt import decode_jwt

auth_routes = Blueprint("auth_routes", __name__)

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()  #Generates new salt
    hashed = bcrypt.hashpw(password.encode(), salt)  #Hash password
    return hashed.decode()  #Convert bytes to a string for storage

@auth_routes.route("/api/auth/password_check", methods=["POST"])
def check_password():
    from api.routes.users import get_user  #Import inside function to avoid circular dependency

    #Get password passed from frontend, entered by user
    data = request.json
    unhashed_password = data.get("password")

    token = request.cookies.get("auth_token")
    if not token:
        return jsonify({"error": "No authentication token found"}), 401

    decoded_token = decode_jwt(token)
    if not decoded_token:
        return jsonify({"error": "Invalid or expired token"}), 401

    #Get user ID and user's info from that
    current_user_id = decoded_token.get("user_id")
    user_response = get_user(current_user_id)[0]
    user_data = json.loads(user_response.data.decode("utf-8"))

    #Get password_hash from user logging in
    password_hash = user_data[0]["password_hash"]

    #Return match based on hashed password decoding
    is_match = bcrypt.checkpw(unhashed_password.encode(), password_hash.encode())

    return jsonify({"match": is_match}), 200