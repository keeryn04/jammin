from flask import Blueprint, app, jsonify, request, session, redirect, url_for
from flask_cors import CORS
from spotipy.oauth2 import SpotifyOAuth
import os
import requests
from dotenv import load_dotenv
import uuid
load_dotenv()

import logging
import json
logging.basicConfig(level=logging.DEBUG)

from api.database_connector import get_db_connection

spotify_routes = Blueprint("spotify_routes", __name__)

API_ACCESS_KEY = os.getenv('API_ACCESS_KEY', 'key')
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
app.secret_key = os.getenv("FLASK_SECRET_KEY")

SCOPE = "user-library-read user-read-private playlist-read-private user-top-read"

sp_oauth = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope=SCOPE
)

#Apply API key to backend access
def require_api_key(f):
    def decorated_function(*args, **kwargs):
        api_key = request.args.get("api_key")
        if api_key != API_ACCESS_KEY:
            return jsonify({"error": "Unauthorized"}), 403
        return f(*args, **kwargs)
    return decorated_function

# Spotify Authentication Routes
@spotify_routes.route("/spotify/login")
def spotify_login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@spotify_routes.route("/spotify/callback")
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

@spotify_routes.route("/fetch_spotify_data")
def fetch_spotify_data():
    access_token = session.get("spotify_access_token")
    
    if not access_token:
        return jsonify({"error": "No Spotify access token"}), 401
    
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get("https://api.spotify.com/v1/me", headers=headers)
    user_profile = response.json()

    top_artists = requests.get("https://api.spotify.com/v1/me/top/artists?limit=10", headers=headers).json()
    top_tracks = requests.get("https://api.spotify.com/v1/me/top/tracks?limit=5", headers=headers).json()

    images = user_profile.get("images", [])
    profile_image = images[0]["url"] if images and "url" in images[0] else "profile.png"

    spotify_data = {
        "spotify_id": user_profile.get("id"),
        "top_songs": [track["name"] for track in top_tracks.get("items", [])],
        "top_songs_pictures": [track["album"]["images"][0]["url"] if track["album"]["images"] else "" for track in top_tracks.get("items", [])],
        "top_artists": [artist["name"] for artist in top_artists.get("items", [])],
        "top_artists_pictures": [artist["images"][0]["url"] if artist["images"] else "" for artist in top_artists.get("items", [])],
        "top_genres": list(set(
            genre 
            for artist in top_artists.get("items", []) 
            for genre in artist.get("genres", [])
        )),
        "top_genres_pictures": ["" for _ in range(len(set(
            genre 
            for artist in top_artists.get("items", []) 
            for genre in artist.get("genres", [])
        )))],
        "profile_name": user_profile.get("display_name"),
        "profile_image": profile_image,
    }

    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500

        #Check if user exists
        existing_user_response = conn.table("users").select("user_id").eq("spotify_id", spotify_data["spotify_id"]).execute()

        if existing_user_response.data: #Existing user
            user_id = existing_user_response.data[0]["user_id"]
        else: #New user
            user_id = str(uuid.uuid4())
            response = conn.table("users").upsert({
                "user_id": user_id,
                "username": spotify_data.get("profile_name", "unknown_user"),
                "email": f"{spotify_data['spotify_id']}@example.com",
                "password_hash": "dummy_password",
                "age": 18,
                "bio": ""
            }).execute()

            if isinstance(response, dict) and "error" in response:
                raise Exception(response["error"]["message"])

        user_data_id = str(uuid.uuid4())
        response = conn.table("users_music_data").upsert({
            "user_data_id": user_data_id,
            "user_id": user_id,
            "spotify_id": spotify_data["spotify_id"],
            "top_songs": ", ".join(spotify_data["top_songs"]),
            "top_songs_pictures": ", ".join(spotify_data["top_songs_pictures"]),
            "top_artists": ", ".join(spotify_data["top_artists"]),
            "top_artists_pictures": ", ".join(spotify_data["top_artists_pictures"]),
            "top_genres": ", ".join(spotify_data["top_genres"]),
            "top_genres_pictures": ", ".join(spotify_data["top_genres_pictures"]),
            "profile_name": spotify_data["profile_name"],
            "profile_image": spotify_data["profile_image"]
        }).execute()

        if isinstance(response, dict) and "error" in response:
            raise Exception(response["error"]["message"])

        return jsonify({"message": "Spotify data added or updated successfully"}), 201

    except Exception as err:
        return jsonify({"error": f"Database error: {err}"}), 500