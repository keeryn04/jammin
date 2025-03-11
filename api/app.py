from flask import Flask, jsonify, request, session
from flask_session import Session
from flask_cors import CORS
from api.routes.spotify import spotify_routes
from api.routes.users import user_routes
from api.routes.user_settings import user_setting_routes
from api.routes.swipes import swipes_routes
from api.routes.matches import matches_routes 
from api.routes.user_data import user_data_routes
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure Flask session
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = os.getenv("FLASK_SECRET_KEY", "key")
Session(app)
CORS(app)

# Register Blueprints
app.register_blueprint(spotify_routes)
app.register_blueprint(user_routes)
app.register_blueprint(user_setting_routes)
app.register_blueprint(matches_routes)
app.register_blueprint(swipes_routes)
app.register_blueprint(user_data_routes)

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

@app.route("/api/login", methods=["POST"])
def login_user():
    data = request.json
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    session['current_user_id'] = user_id  #Store as session variable (Login)
    return jsonify({"message": "Login successful", "user_id": user_id}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    app.config["DEBUG"] = True