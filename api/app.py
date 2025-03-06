from flask import Flask, request, redirect, session, jsonify
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
# Set the secret key
app.secret_key = os.getenv("FLASK_SECRET_KEY", "supersecretkey")

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

SCOPE = "user-library-read user-read-private playlist-read-private user-top-read user-read-playback-state user-modify-playback-state"

sp_oauth = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope=SCOPE
)

@app.route("/")
def home():
    return jsonify({"message": "API is working!"})

@app.route("/login")
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return jsonify({"error": "Authorization failed"}), 400

    token_info = sp_oauth.get_access_token(code)
    session["token_info"] = token_info

    return redirect("/profile")

@app.route("/profile")
def profile():
    try:
        token_info = session.get("token_info", None)
        if not token_info:
            return jsonify({"error": "Not authenticated"}), 401

        # Refresh token if expired
        if sp_oauth.is_token_expired(token_info):
            token_info = sp_oauth.refresh_access_token(token_info["refresh_token"])
            session["token_info"] = token_info

        sp = spotipy.Spotify(auth=token_info["access_token"])

        # Fetch user profile
        user_info = sp.current_user()

        # Fetch top tracks
        top_tracks = sp.current_user_top_tracks(limit=5)["items"] if sp.current_user_top_tracks(limit=5) else []

        # Fetch top artists
        top_artists = sp.current_user_top_artists(limit=5)["items"] if sp.current_user_top_artists(limit=5) else []

        # Fetch user playlists
        playlists = sp.current_user_playlists()["items"] if sp.current_user_playlists() else []

        # Fetch currently playing track (handle errors)
        currently_playing = None
        try:
            playback = sp.current_playback()
            if playback and playback["item"]:
                currently_playing = playback["item"]["name"]
        except Exception as e:
            currently_playing = "No song playing"

        return jsonify({
            "user": user_info,
            "top_tracks": [{"name": t["name"], "artist": t["artists"][0]["name"]} for t in top_tracks],
            "top_artists": [{"name": a["name"], "genres": a["genres"]} for a in top_artists],
            "playlists": [{"name": p["name"], "id": p["id"]} for p in playlists],
            "currently_playing": currently_playing
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/play", methods=["GET"])
def play_default_song():
    token_info = session.get("token_info", None)
    if not token_info:
        return jsonify({"error": "Not authenticated"}), 401

    # Refresh token if expired
    if sp_oauth.is_token_expired(token_info):
        token_info = sp_oauth.refresh_access_token(token_info["refresh_token"])
        session["token_info"] = token_info

    sp = spotipy.Spotify(auth=token_info["access_token"])

    track_id = "5ZLUm9eab8y3tqQ1OhQSHI"  # Default song

    try:
        sp.start_playback(uris=[f"spotify:track:{track_id}"])
        return jsonify({"message": f"Now playing: {track_id}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
