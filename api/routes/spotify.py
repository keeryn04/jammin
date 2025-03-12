from flask import Blueprint, app, jsonify, request, session, redirect, url_for
from flask_cors import CORS
from spotipy.oauth2 import SpotifyOAuth
import os
import requests
from dotenv import load_dotenv
import mysql.connector
import uuid
load_dotenv()

import logging

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
    scope=SCOPE,
    cache_path=None
)

# Spotify Authentication Routes
@spotify_routes.route("/api/spotify/login")
def spotify_login():
    print("Spotify Route Accessed")
    auth_url = sp_oauth.get_authorize_url()
    print(f"Redirecting to: {auth_url}")
    return redirect(auth_url) 
    #jsonify({"success": True, "redirect_url": auth_url})

@spotify_routes.route("/api/spotify/callback")
def spotify_callback():
    print("Redirected to Callback")
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
    return redirect("/api/fetch_spotify_data")

@spotify_routes.route("/api/fetch_spotify_data")
def fetch_spotify_data():
    access_token = session.get("spotify_access_token")
    print(session.get("spotify_access_token"))
    
    if access_token == None:
        return redirect("http://localhost:5173/login"), 402
    
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
            return redirect("http://localhost:5173/login"), 500

        #Save spotify ID
        spotify_id = spotify_data["spotify_id"]

        #Check if user exists
        user_id = session.get('current_user_id')

        if not user_id:
            return jsonify({"error": "User not logged in"}), 401
        
        response = conn.table("users").select("user_data_id").eq("user_id", user_id).execute()

        if not response.data:
            return redirect("http://localhost:5173/login"), 404
        
        user_data_id = response.data[0]["user_data_id"]
        
        response = conn.table("users_music_data").upsert({
                "user_data_id": user_data_id,
                "spotify_id": spotify_id,
                "top_songs": ", ".join(spotify_data["top_songs"]),
                "top_songs_pictures": ", ".join(spotify_data["top_songs_pictures"]),
                "top_artists": ", ".join(spotify_data["top_artists"]), 
                "top_artists_pictures": ", ".join(spotify_data["top_artists_pictures"]),
                "top_genres": ", ".join(spotify_data["top_genres"]),
                "top_genres_pictures": ", ".join(spotify_data["top_genres_pictures"]),
                "profile_name": spotify_data.get("profile_name"), 
                "profile_image": spotify_data.get("profile_image")
            }).execute()

        if isinstance(response, dict) and "error" in response:
            raise Exception(response["error"]["message"])

        return redirect("http://localhost:5173/login"), 201

    except Exception as err:
        return jsonify({"error": f"Database error: {err}"}), 500
