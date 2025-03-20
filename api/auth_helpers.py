import bcrypt
from flask import Blueprint, jsonify, request

from api.jwt import decode_jwt

auth_routes = Blueprint("auth_routes", __name__)

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()  #Generates new salt
    hashed = bcrypt.hashpw(password.encode(), salt)  #Hash password
    return hashed.decode()  #Convert bytes to a string for storage

@auth_routes.route("/api/auth/password_check/<password>", methods=["POST"])
def check_password(password: str, hashed_password: str) -> bool:
    from api.routes.users import get_user #Import inside method to avoid circular dependency
    #Fetch entered user_id
    data = request.json
    unhashed_password = data["password"]

    token = request.cookies.get("auth_token")

    if not token:
        return jsonify({"error": "No authentication token found"}), 401

    decoded_token = decode_jwt(token)

    if not decoded_token:
        return jsonify({"error": "Invalid or expired token"}), 401

    current_user_id = decoded_token.get("user_id")
    hashed_password = get_user(current_user_id).get("password_hash")
    
    return bcrypt.checkpw(unhashed_password.encode(), hashed_password.encode()), 200