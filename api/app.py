from flask import Flask, jsonify, make_response, request, session
from flask_cors import CORS
from api.jwt import generate_jwt, decode_jwt
from api.routes.spotify import spotify_routes
from api.routes.users import user_routes
from api.routes.user_settings import user_setting_routes
from api.routes.swipes import swipes_routes
from api.routes.matches import matches_routes 
from api.routes.user_data import user_data_routes
from api.routes.gpt import openai_routes
import os
from dotenv import load_dotenv

from routes.gpt import openai_routes



# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure Flask session
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_COOKIE_SAMESITE"] = None  #Allows cross-site cookies
app.config["SESSION_COOKIE_SECURE"] = True  #Only over HTTPS
app.secret_key = os.getenv("FLASK_SECRET_KEY")
CORS(app, supports_credentials=True)

# Register Blueprints
app.register_blueprint(spotify_routes)
app.register_blueprint(user_routes)
app.register_blueprint(user_setting_routes)
app.register_blueprint(matches_routes)
app.register_blueprint(swipes_routes)
app.register_blueprint(user_data_routes)
app.register_blueprint(openai_routes)

#API Key Authentication
API_ACCESS_KEY = os.getenv('API_ACCESS_KEY')

#Apply API key to backend access
def require_api_key(f):
    def decorated_function(*args, **kwargs):
        api_key = request.args.get("api_key")
        if api_key != API_ACCESS_KEY:
            return jsonify({"error": "Unauthorized"}), 403
        return f(*args, **kwargs)
    return decorated_function

#Default path
@app.route("/", methods=["GET"])
def default_api():
    return jsonify({"message": "API is working!"})

#For storing current session ID after login
@app.route("/api/login", methods=["POST"])
def login_user():
    data = request.json
    user_id = data.get("user_id")
    print(f"User {user_id} logged in!")

    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400
    
    jwt_token = generate_jwt(user_id)

    # Set the JWT token in an HTTP-only cookie, allows access of user_id elsewhere in program
    response = make_response(jsonify({"message": "Login successful", "user_id": user_id}))
    response.set_cookie("auth_token", jwt_token, httponly=True, secure=True, samesite="Strict", max_age=3600)
    
    return response, 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    app.config["DEBUG"] = True