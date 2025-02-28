from flask import Flask, jsonify, request, session, redirect, url_for
from flask_cors import CORS
from spotipy.oauth2 import SpotifyOAuth
import mysql.connector
import os
import requests
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "key")

API_ACCESS_KEY = os.getenv('API_ACCESS_KEY', 'key')
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

SCOPE = "user-library-read user-read-private playlist-read-private user-top-read"

sp_oauth = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope=SCOPE
)

#Get environment variables for MySQL connection
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
DB_NAME = os.getenv('DB_NAME', 'jammin_db')

#Test database connection
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None

#Apply API key to backend access
def require_api_key(f):
    def decorated_function(*args, **kwargs):
        api_key = request.args.get("api_key")
        if api_key != API_ACCESS_KEY:
            return jsonify({"error": "Unauthorized"}), 403
        return f(*args, **kwargs)
    return decorated_function

# Spotify Authentication Routes
@app.route("/spotify/login")
def spotify_login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route("/spotify/callback")
def spotify_callback():
    code = request.args.get("code")
    token_url = "https://accounts.spotify.com/api/token"
    response = requests.post(
        token_url,
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": SPOTIFY_REDIRECT_URI,
            "client_id": SPOTIFY_CLIENT_ID,
            "client_secret": SPOTIFY_CLIENT_SECRET,
        },
    )
    data = response.json()
    session["spotify_access_token"] = data.get("access_token")
    return redirect("/fetch_spotify_data")

@app.route("/fetch_spotify_data")
def fetch_spotify_data():
    access_token = session.get("spotify_access_token")
    if not access_token:
        return jsonify({"error": "No Spotify access token"}), 401

    headers = {"Authorization": f"Bearer {access_token}"}
    user_profile = requests.get("https://api.spotify.com/v1/me", headers=headers).json()
    top_artists = requests.get("https://api.spotify.com/v1/me/top/artists?limit=10", headers=headers).json()
    top_tracks = requests.get("https://api.spotify.com/v1/me/top/tracks?limit=5", headers=headers).json()

    images = user_profile.get("images", [])
    profile_image = images[0]["url"] if images else ""

    spotify_data = {
        "spotify_id": user_profile.get("id"),
        "top_songs": [track["name"] for track in top_tracks.get("items", [])],
        "top_artists": [artist["name"] for artist in top_artists.get("items", [])],
        "top_genres": list(set(
            genre 
            for artist in top_artists.get("items", []) 
            for genre in artist.get("genres", [])
        )),
        "profile_name": user_profile.get("display_name"),
        "profile_image": profile_image,
    }

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    cursor = conn.cursor()

    # Check if a user with this spotify_id already exists in the users table
    cursor.execute("SELECT COUNT(*) FROM users WHERE spotify_id = %s", (spotify_data["spotify_id"],))
    result = cursor.fetchone()
    if result[0] == 0:
        # Insert new user record with default values if it doesn't exist
        new_user_query = """
        INSERT INTO users (user_id, spotify_id, username, email, password_hash, age, bio)
        VALUES (UUID(), %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(new_user_query, (
            spotify_data["spotify_id"],
            spotify_data["profile_name"] or "unknown_user",
            f"{spotify_data['spotify_id']}@example.com",
            "dummy_password",  # Replace with a secure default or handle appropriately
            18,                # Default age (must be >= 13)
            ""
        ))
        conn.commit()

    # Insert or update spotify_data
    query = (
        "INSERT INTO spotify_data (spotify_id, top_songs, top_artists, top_genres, profile_name, profile_image) "
        "VALUES (%s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE "
        "top_songs=VALUES(top_songs), top_artists=VALUES(top_artists), "
        "top_genres=VALUES(top_genres), profile_name=VALUES(profile_name), profile_image=VALUES(profile_image)"
    )
    cursor.execute(query, (
        spotify_data["spotify_id"],
        ", ".join(spotify_data["top_songs"]),
        ", ".join(spotify_data["top_artists"]),
        ", ".join(spotify_data["top_genres"]),
        spotify_data["profile_name"],
        spotify_data["profile_image"]
    ))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Spotify data fetched and stored successfully"})

#Default path
@app.route("/", methods=["GET"])
def default_api():
    return jsonify({"message": "API is working!"})

# -------------------- USERS --------------------
@app.route("/api/users", methods=["GET"])
def get_users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(rows)
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500

@app.route("/api/users", methods=["POST"])
def add_user():
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO users (user_id, spotify_id, username, email, password_hash, age, bio) 
        VALUES (UUID(), %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (data["spotify_id"], data["username"], data["email"], data["password_hash"], data["age"], data.get("bio")))
        
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "User added successfully"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500

@app.route("/api/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": "User deleted successfully"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500

@app.route("/api/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        UPDATE users 
        SET spotify_id=%s, username=%s, email=%s, password_hash=%s, age=%s, bio=%s 
        WHERE user_id=%s
        """
        cursor.execute(query, (data["spotify_id"], data["username"], data["email"], data["password_hash"], data["age"], data.get("bio"), user_id))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "User updated successfully"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500

# -------------------- USER SETTINGS --------------------
@app.route("/api/user_settings", methods=["GET"])
def get_user_settings():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_settings")
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(rows)
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500

@app.route("/api/user_settings/<user_id>", methods=["PUT"])
def update_user_settings(user_id):
    try:
        data = request.json
        conn = get_db_connection()
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

# -------------------- MATCHES --------------------
@app.route("/api/matches", methods=["GET"])
def get_matches():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM matches")
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(rows)
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500

@app.route("/api/matches", methods=["POST"])
def add_match():
    try:
        data = request.json
        conn = get_db_connection()
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

@app.route("/api/matches/<match_id>", methods=["DELETE"])
def delete_match(match_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM matches WHERE match_id = %s", (match_id,))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": "Match deleted successfully"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500

# -------------------- SWIPES --------------------
@app.route("/api/swipes", methods=["GET"])
def get_swipes():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM swipes")
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(rows)
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500

@app.route("/api/swipes", methods=["POST"])
def add_swipe():
    try:
        data = request.json
        conn = get_db_connection()
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

@app.route("/api/swipes/<swipe_id>", methods=["DELETE"])
def delete_swipe(swipe_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM swipes WHERE swipe_id = %s", (swipe_id,))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": "Swipe deleted successfully"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500

# -------------------- SPOTIFY DATA --------------------
@app.route("/api/spotify_data", methods=["GET"])
def get_spotify_data():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM spotify_data")
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(rows)
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500

@app.route("/api/spotify-data", methods=["POST"])
def add_spotify_data():
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO spotify_data (spotify_id, top_songs, top_artists, top_genres, profile_link) 
        VALUES (UUID(), %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (data["spotify_id"], data["top_songs"], data["top_artists"], data["top_genres"], data["profile_name"], data["profile_link"]))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Spotify entry added successfully"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    
@app.route("/api/spotify_data/<spotify_id>", methods=["DELETE"])
def delete_spotify_data(spotify_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM spotify_data WHERE spotify_id = %s", (spotify_id,))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": "Spotify data deleted successfully"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    
@app.route("/api/spotify_data/<spotify_id>", methods=["PUT"])
def update_spotify_data(spotify_id):
    try:
        data = request.json

        top_songs = data.get("top_songs")
        top_artists = data.get("top_artists")
        top_genres = data.get("top_genres")
        profile_name = data.get("profile_name")
        profile_image = data.get("profile_image")
        
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("UPDATE spotify_data SET top_songs=%s, top_artists=%s, top_genres=%s, profile_name=%s, profile_image=%s WHERE spotify_id=%s", 
                       (top_songs, top_artists, top_genres, profile_name, profile_image, spotify_id))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": "Spotify data updated successfully"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    app.config["DEBUG"] = True