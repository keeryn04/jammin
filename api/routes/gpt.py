from flask import Blueprint, app, jsonify, request, session, redirect, url_for
from flask_cors import CORS
from spotipy.oauth2 import SpotifyOAuth
import mysql.connector
import os
import requests
from dotenv import load_dotenv
import uuid
import openai
import json

load_dotenv()
from database_connector import get_db_connection

API_ACCESS_KEY = os.getenv('API_ACCESS_KEY', 'key')
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=openai.api_key)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
openai_routes = Blueprint("openai_routes", __name__)

def require_api_key(f):
    def decorated_function(*args, **kwargs):
        api_key = request.args.get("api_key")
        if api_key != API_ACCESS_KEY:
            return jsonify({"error": "Unauthorized"}), 403
        return f(*args, **kwargs)
    return decorated_function

@openai_routes.route("/chattesting", methods=["GET"])
def run_ChatQuery():    
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


