from flask import Flask, request, jsonify
from flask_cors import CORS
from .data_layer.omdb_api import search_movies
from .data_layer.database import get_watchlist_from_db, add_to_watchlist_db, remove_from_watchlist_db, get_movie_by_title_db

app = Flask(__name__)
CORS(app)

@app.route('/watchlist', methods=['GET'])
def get_watchlist():
    try:
        return jsonify(get_watchlist_from_db()), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch watchlist", "details": str(e)}), 500

@app.route('/watchlist', methods=['POST'])
def add_watchlist():
    try:
        data = request.json
        # Validation: Ensure title is provided
        if not data or 'title' not in data:
            return jsonify({"error": "Title is required"}), 400

        # Duplicate Handling
        if get_movie_by_title_db(data['title']):
            return jsonify({"error": "Movie already exists in watchlist"}), 409

        add_to_watchlist_db(data.get('title'), data.get('year', 'N/A'))
        return jsonify({"message": "Successfully added"}), 201
    except Exception as e:
        return jsonify({"error": "Failed to add movie", "details": str(e)}), 500

@app.route('/watchlist/<string:title>', methods=['DELETE'])
def delete_movie(title):
    try:
        # Check if movie exists before trying to delete
        if not get_movie_by_title_db(title):
            return jsonify({"error": "Movie not found"}), 404
        
        remove_from_watchlist_db(title)
        return jsonify({"message": "Successfully deleted"}), 200
    except Exception as e:
        return jsonify({"error": "Failed to delete movie", "details": str(e)}), 500

@app.route('/search', methods=['GET'])
def search():
    try:
        query = request.args.get('query')
        if not query:
            return jsonify({"error": "Query parameter required"}), 400
        return jsonify(search_movies(query)), 200
    except Exception as e:
        return jsonify({"error": "Search failed", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)