from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

# Use absolute path to ensure we always hit the correct DB
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'movies.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ROUTE: Get all movies in watchlist
@app.route('/watchlist', methods=['GET'])
def get_watchlist():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM watchlist').fetchall()
    conn.close()
    # Convert sqlite3 rows to a list of dictionaries
    watchlist = [dict(row) for row in rows]
    return jsonify(watchlist)

# ROUTE: Add a movie
@app.route('/watchlist/add', methods=['POST'])
def add_to_watchlist():
    data = request.get_json()
    name = data.get('name')
    year = data.get('year')

    if not name or not year:
        return jsonify({"message": "Name and Year are required!"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO watchlist (title, year) VALUES (?, ?)", (name, year))
    conn.commit()
    conn.close()
    return jsonify({"message": f"Movie '{name}' added successfully!"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)