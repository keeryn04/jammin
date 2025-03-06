from flask import Flask, request, redirect, session, jsonify
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import openai
import json
from pydantic import BaseModel
app = Flask(__name__)
"""
SPOTIPY_CLIENT_ID = "ec7d412a119243419b8118fb6cbc8529"
SPOTIPY_CLIENT_SECRET = ""
SPOTIPY_REDIRECT_URI = "http://localhost:5000/callback"

SCOPE = "user-library-read user-read-private playlist-read-private user-top-read user-read-playback-state user-modify-playback-state"

sp_oauth = SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=SCOPE
)
"""
@app.route("/")
def home():
    return jsonify({"message": "API is working!"})
"""
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
    """


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
