from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "API is working!"})

@app.route("/hello", methods=["GET"])
def hello():
    return jsonify({"message": "Hello from Flask!"})