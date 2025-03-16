import os
import jwt
import datetime
from flask import Blueprint, Flask, request, jsonify
import jwt

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
jwt_routes = Blueprint("jwt_routes", __name__)

def generate_jwt(user_id, user_data_id):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    payload = {
        "user_id": user_id,
        "user_data_id": user_data_id,
        "exp": expiration
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")

def update_jwt(old_token, new_claims):
    try:
        decoded_token = jwt.decode(old_token, JWT_SECRET_KEY, algorithms=["HS256"], options={"verify_exp": False})
        decoded_token.update(new_claims)
        decoded_token["exp"] = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        return jwt.encode(decoded_token, JWT_SECRET_KEY, algorithm="HS256")
    except jwt.InvalidTokenError:
        return None

def decode_jwt(token):
    try:
        return jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

@jwt_routes.route("/api/auth/check", methods=["GET"])
def check_auth():
    token = request.cookies.get("auth_token")  #Read cookie from request
    if not token:
        return jsonify({"authenticated": False}), 401
    
    decoded = decode_jwt(token)
    if not decoded:
        return jsonify({"authenticated": False, "error": "Invalid or expired token"}), 401
    
    return jsonify({"authenticated": True, "user": decoded})

