from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  #Allows frontend to access the backend

@app.route("/api/hello", methods=["GET"])
def hello():
    return jsonify({"message": "Hello from Flask!"})