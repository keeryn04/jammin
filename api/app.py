from flask import Flask, jsonify, request, session
from flask_session import Session
from flask_cors import CORS
from routes.spotify import spotify_routes
from database_connector import get_db_connection
import os
import mysql.connector
import uuid
from dotenv import load_dotenv
import openai
import json

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

# API Key Authentication
API_ACCESS_KEY = os.getenv('API_ACCESS_KEY', 'key')

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
@app.route("/api/user_data", methods=["GET"])
def get_user_data():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users_music_data")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(rows)
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    
#For fetching data to send to ChatGPT
@app.route("/api/user_data/<user_id>", methods=["GET"])
def get_user_music_data_by_id(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users_music_data WHERE user_id = %s", (user_id,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        if rows:
            response = {
                "user_id": rows[0]["user_id"],
                "music_profile": {
                    "top_songs": rows[0]["top_songs"],
                    "top_artists": rows[0]["top_artists"],
                    "top_genres": rows[0]["top_genres"]
                }
            }
        else:
            response = {"error": "User not found"}

        return jsonify(response)
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500

#For fetching specific number of top artists  
@app.route("/api/user_data/<user_id>/<int:limit>", methods=["GET"])
def get_user_top_artists_by_id(user_id, limit):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users_music_data WHERE user_id = %s", (user_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            top_artists_list = row["top_artists"].split(", ")[:limit]
            top_artists_pictures_list = row["top_artists_pictures"].split(", ")[:limit]
            response = {
                "user_id": user_id,
                "top_artists": top_artists_list,
                "top_artists_pictures": top_artists_pictures_list
            }
        else:
            response = {"error": "User not found"}

        return jsonify(response)
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500

@app.route("/api/user_data", methods=["POST"])
def add_user_data():
    try:
        data = request.json
        user_data_id = str(uuid.uuid4())
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO users_music_data (user_data_id, user_id, top_songs, top_songs_pictures, 
                                      top_artists, top_artists_pictures, top_genres, top_genres_pictures, 
                                      profile_name, profile_image) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            user_data_id, data["user_id"], data["top_songs"], data["top_songs_pictures"],
            data["top_artists"], data["top_artists_pictures"], data["top_genres"], data["top_genres_pictures"],
            data["profile_name"], data["profile_image"]
        ))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Music entry added successfully"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500

@app.route("/api/user_data/<user_id>", methods=["DELETE"])
def delete_user_data(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users_music_data WHERE user_id = %s", (user_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Music data deleted successfully"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500

@app.route("/api/user_data/<user_id>", methods=["PUT"])
def update_user_data(user_id):
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        UPDATE users_music_data 
        SET top_songs=%s, top_songs_pictures=%s, 
            top_artists=%s, top_artists_pictures=%s, 
            top_genres=%s, top_genres_pictures=%s, 
            profile_name=%s, profile_image=%s 
        WHERE user_id=%s
        """
        cursor.execute(query, (
            data.get("top_songs"), data.get("top_songs_pictures"),
            data.get("top_artists"), data.get("top_artists_pictures"),
            data.get("top_genres"), data.get("top_genres_pictures"),
            data.get("profile_name"), data.get("profile_image"), user_id
        ))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Music data updated successfully"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500

@app.route("/chattesting", methods=["GET"])
def run_ChatQuery():    
    openai.api_key = ""
    client = openai.OpenAI(api_key=openai.api_key)

    messages = [ #defines the role of
        {"role": "system", "content": 
        """You are a matchmaking compatibility score generator for music preferences. You will be given a list of users, each with their favorite songs, artists, and genres. 
        The first user in the list is the REFERENCE user. You will match them with all others and EXCLUDE them from the output.
        The output should be in JSON format.
        Example input:
        [
        {'userid':'0', 'topSongs':['SongA'], 'topArtists':['ArtistA'], 'topGenres':['GenreA']},
        {'userid':'72', 'topSongs':['SongB'], 'topArtists':['ArtistB'], 'topGenres':['GenreB']}
        ]
        Example output:
        [
            {'userID':'72', 'compatibility_score': 75,'reasoning':'They have similar favourite artists, and similar genres'}
        ]
        """}]

    message = [{"userid":"0", 
                "topSongs":["Hotline Bling","Be Nice 2 Me","Stephanie", "did i tell u that i miss u","Beanie"],
                "topArtists":["Drake","Malcolm Todd","Bladee","BROCKHAMPTON","d4vd"],
                "topGenres":["HipHop","Rap","Indie Pop","R&B","Alt HipHop"]},
                {
                "userid": "5",
                "topSongs": ["Obedient", "Super Rich Kids", "Stephanie", "NOKIA", "Pink + White"],
                "topArtists": ["Bladee", "Frank Ocean", "MarQ", "Lauryn Hill", "Kanye West"],
                "topGenres": ["R&B", "Alt HipHop", "Rap", "HipHop", "Indie Pop"]
                },
                {
                "userid": "4",
                "topSongs": ["Money Trees", "N95", "Alright", "Praise The Lord", "Power"],
                "topArtists": ["Kendrick Lamar", "J. Cole", "A$AP Rocky", "Kanye West", "Jay-Z"],
                "topGenres": ["HipHop", "Rap", "Conscious Rap", "Boom Bap", "Alternative HipHop"]
                },
                {
                "userid": "3",
                "topSongs": ["The Less I Know The Better", "Electric Feel", "Somebody Else", "Loving Is Easy", "West Coast"],
                "topArtists": ["Tame Impala", "MGMT", "The 1975", "Rex Orange County", "Lana Del Rey"],
                "topGenres": ["Indie Rock", "Psychedelic Pop", "Alternative", "Dream Pop", "Indie Pop"]
                },
                {
                "userid": "1",
                "topSongs": ["Master of Puppets", "Paranoid", "Ace of Spades", "Holy Wars", "Raining Blood"],
                "topArtists": ["Metallica", "Black Sabbath", "Motörhead", "Megadeth", "Slayer"],
                "topGenres": ["Heavy Metal", "Thrash Metal", "Hard Rock", "Classic Metal", "Speed Metal"]
                },
                {
                "userid": "2",
                "topSongs": ["Clair de Lune", "Nocturne Op. 9 No. 2", "Gymnopédie No. 1", "Moonlight Sonata", "Rhapsody in Blue"],
                "topArtists": ["Claude Debussy", "Frédéric Chopin", "Erik Satie", "Ludwig van Beethoven", "George Gershwin"],
                "topGenres": ["Classical", "Romantic", "Impressionist", "Baroque", "Jazz-Classical Fusion"]
                }]#here ideally would run get requests from spotify for specific users
    message_content = json.dumps(message)
    messages.append({"role": "user", "content": message_content})
    chat = client.beta.chat.completions.parse(
        model="gpt-3.5-turbo",
        messages=messages,
        response_format={"type": "json_object"}
    )
    reply = chat.choices[0].message.content
    return jsonify(json.loads(reply))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    app.config["DEBUG"] = True