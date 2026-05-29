import sys
import os
from flask import Flask, request, jsonify

# Add the project root directory to sys.path so we can import data_layer
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_layer.database import init_db, add_to_watchlist, get_watchlist

app = Flask(__name__)

# Initialize your database
init_db()

@app.route('/watchlist/get', methods=['GET'])
def get_movies():
    return jsonify(get_watchlist())

@app.route('/watchlist/add', methods=['POST'])
def add_movie():
    # Capture the full JSON body
    data = request.json
    
    # Pass the entire data dictionary to the database function
    # This prevents the "string indices" error
    add_to_watchlist(data)
    
    return jsonify({"message": "Movie added successfully!"})

if __name__ == '__main__':
    app.run(debug=True)