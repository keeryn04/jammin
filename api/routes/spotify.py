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

from database_connector import get_db_connection

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

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    cursor = conn.cursor()

    cursor.execute("SELECT user_id FROM users WHERE spotify_id = %s", (spotify_data["spotify_id"],))
    result = cursor.fetchone()
    if result is None:
        new_user_id = str(uuid.uuid4())
        new_user_query = """
        INSERT INTO users (user_id, username, email, password_hash, age, bio)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(new_user_query, (
            new_user_id,
            spotify_data["profile_name"] or "unknown_user",
            f"{spotify_data['spotify_id']}@example.com",
            "dummy_password",  
            18,                
            ""
        ))
        user_id = new_user_id
        conn.commit()
    else:
        user_id = result[0]

    query = """
        INSERT INTO users_music_data (user_data_id, user_id, top_songs, top_songs_pictures, 
                                      top_artists, top_artists_pictures, top_genres, top_genres_pictures, 
                                      profile_name, profile_image) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE 
        top_songs=VALUES(top_songs), top_songs_pictures=VALUES(top_songs_pictures),
        top_artists=VALUES(top_artists), top_artists_pictures=VALUES(top_artists_pictures),
        top_genres=VALUES(top_genres), top_genres_pictures=VALUES(top_genres_pictures),
        profile_name=VALUES(profile_name), profile_image=VALUES(profile_image)
        """
    cursor.execute(query, (
        str(uuid.uuid4()),
        user_id,
        ", ".join(spotify_data["top_songs"]),
        ", ".join(spotify_data["top_songs_pictures"]),
        ", ".join(spotify_data["top_artists"]),
        ", ".join(spotify_data["top_artists_pictures"]),
        ", ".join(spotify_data["top_genres"]),
        ", ".join(spotify_data["top_genres_pictures"]),
        spotify_data["profile_name"],
        spotify_data["profile_image"]
    ))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Spotify data fetched and stored successfully"})