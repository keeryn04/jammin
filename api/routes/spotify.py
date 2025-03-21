from flask import Blueprint, app, jsonify, request, redirect, make_response
from spotipy.oauth2 import SpotifyOAuth
import os
import requests
from dotenv import load_dotenv
load_dotenv()
from database.database_connector import get_db_connection
from api.jwt import decode_jwt, update_jwt

spotify_routes = Blueprint("spotify_routes", __name__)

VERCEL_URL = os.getenv('VITE_VERCEL_URL')
API_ACCESS_KEY = os.getenv('API_ACCESS_KEY')
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
app.secret_key = os.getenv("FLASK_SECRET_KEY")

SCOPE = "user-library-read user-read-private playlist-read-private user-top-read"

sp_oauth = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=SCOPE,
    cache_path=None
)

#Redirect user to spotify login page
@spotify_routes.route("/api/spotify/login")
def spotify_login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url) 

#Return user back to Jammin
@spotify_routes.route("/api/spotify/callback")
def spotify_callback():
    code = request.args.get("code")

    if not code:
        return jsonify({"error": "Missing authorization code in callback"}), 400

    #Fetch token for data access
    token_url = "https://accounts.spotify.com/api/token"
    response = requests.post(
        token_url,
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": SPOTIPY_REDIRECT_URI,
            "client_id": SPOTIFY_CLIENT_ID,
            "client_secret": SPOTIFY_CLIENT_SECRET,
        },
    )

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch access token", "details": response.text}), 400

    #Save Spotify auth. token in cookie
    data = response.json()
    spotify_access_token = data.get("access_token")
    if not spotify_access_token:
        return jsonify({"error": "Failed to get access token from Spotify"}), 400

    old_token = request.cookies.get("auth_token")

    if not old_token:
        return jsonify({"error": "No auth token found"}), 401

    new_token = update_jwt(old_token, {"spotify_access_token": spotify_access_token})
    
    if new_token is None:
        return jsonify({"error": "Failed to update JWT token"}), 500
    
    if isinstance(new_token, str):
        response = make_response(redirect(f"{VERCEL_URL}/api/fetch_spotify_data"))
        response.set_cookie("auth_token", new_token, httponly=True, secure=True, samesite="None", max_age=3600)
        return response
    else:
        return jsonify({"error": "Invalid token format"}), 500

#Get spotify data based on token, and save it in database
@spotify_routes.route("/api/fetch_spotify_data")
def fetch_spotify_data():
    token = request.cookies.get("auth_token")

    if not token:
        return jsonify({"error": "No authentication token found"}), 401

    #Decode cookie token
    decoded_token = decode_jwt(token)

    if not decoded_token:
        return jsonify({"error": "Invalid or expired token"}), 401

    #Get spotify token from decoded cookie
    access_token = decoded_token.get("spotify_access_token")
    
    if access_token == None:
        return redirect(f"{VERCEL_URL}/Login"), 401 #Return to login page if error
    
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get("https://api.spotify.com/v1/me", headers=headers)
    user_profile = response.json()

    #Get top songs, top artists, images, etc.
    top_artists = requests.get("https://api.spotify.com/v1/me/top/artists?limit=10", headers=headers).json()
    top_tracks = requests.get("https://api.spotify.com/v1/me/top/tracks?limit=5", headers=headers).json()

    images = user_profile.get("images", [])
    profile_image = images[0]["url"] if images and "url" in images[0] else "https://static.thenounproject.com/png/4530368-200.png"

    #Save spotify data in JSON format
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
            return redirect(f"{VERCEL_URL}/Login"), 500 #Return to login page if database error

        #Save spotify ID
        spotify_id = spotify_data["spotify_id"]

        #Get user_id from cookies
        token = request.cookies.get("auth_token")

        if not token:
            return jsonify({"error": "No authentication token found"}), 401
    
        #Decode cookie token
        decoded_token = decode_jwt(token)
        
        if not decoded_token:
            return jsonify({"error": "Invalid or expired token"}), 401

        #Get current user ID from decoded cookie token
        user_id = decoded_token.get("user_id")

        if not user_id:
            return jsonify({"error": "User not logged in"}), 401
        
        #Fetch user_data_id based on user_id
        response = conn.table("users").select("user_data_id").eq("user_id", user_id).execute()

        if not response.data:
            return redirect(f"{VERCEL_URL}/Login"), 401
        
        #Save user_data_id
        user_data_id = response.data[0]["user_data_id"]
        
        #Update user's spotify data in database
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

        return redirect(f"{VERCEL_URL}/Matching", code=302) #Return back to homepage after saving spotify data

    except Exception as err:
        return jsonify({"error": f"Database error: {err}"}), 500
