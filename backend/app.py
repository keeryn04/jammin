# app.py
from flask import Flask, jsonify

app = Flask(__name__, static_folder='path_to_vite_dist', static_url_path='/')

@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify(message="Hello from Flask!")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
