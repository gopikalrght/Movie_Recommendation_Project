from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
# Enable CORS so your frontend can talk to this backend
CORS(app)

def get_db_connection():
    # Connect to your movies.db
    conn = sqlite3.connect('movies.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/watchlist/add', methods=['POST'])
def add_to_watchlist():
    try:
        data = request.get_json()
        name = data.get('name')
        year = data.get('year')

        if not name or not year:
            return jsonify({"message": "Name and Year are required!"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        
        # FIXED: Using 'title' instead of 'name' to match your database schema
        cursor.execute("INSERT INTO watchlist (title, year) VALUES (?, ?)", (name, year))
        
        conn.commit()
        conn.close()

        return jsonify({"message": f"Movie '{name}' added successfully!"}), 200
    
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    # Running on port 5000
    app.run(debug=True, port=5000)