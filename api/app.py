from flask import Flask, jsonify
import mysql.connector
import os

app = Flask(__name__)

#Get environment variables for MySQL connection
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
DB_NAME = os.getenv('DB_NAME', 'jammin_db')

#Test database connection
def get_db_connection():
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    return conn

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "API is working!"})

#Test fetch
@app.route("/api/data", methods=["GET"])
def get_data():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(rows)
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)