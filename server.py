from flask import Flask, request, jsonify
from data_layer.database import init_db, add_to_watchlist, get_watchlist

app = Flask(__name__)

# TASK 1: Initialize the DB (This creates the file if it doesn't exist)
init_db()

@app.route('/watchlist/add', methods=['POST'])
def add_movie():
    # TASK 2: Use database instead of a Python list
    movie_data = request.json # Expects JSON like {"title": "Inception", "year": "2010"}
    add_to_watchlist(movie_data)
    return jsonify({"status": "success", "message": "Movie added to database"})

@app.route('/watchlist/get', methods=['GET'])
def get_movies():
    # TASK 3: Fetch from database instead of a temporary list
    watchlist = get_watchlist()
    return jsonify(watchlist)

if __name__ == '__main__':
    app.run(debug=True)