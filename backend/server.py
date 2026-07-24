from flask import Flask, request, jsonify
from flask_cors import CORS
from backend.data_layer.database import init_db, get_watchlist_db, add_movie_db, get_movie_by_title_db, delete_movie_db
from backend.data_layer.omdb_api import search_movies

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize the database on startup
init_db()

@app.route('/search', methods=['GET'])
def search_movie():
        query = request.args.get('query')
        if not query:
            return jsonify({"error": "Query parameter is required"}), 400
        
        result = search_movies(query)
        if "error" in result:
            return jsonify(result), 404
            
        return jsonify(result), 200
    

@app.route('/watchlist', methods=['GET'])
def get_watchlist():
    try:
        watchlist = get_watchlist_db()
        return jsonify(watchlist), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch watchlist", "details": str(e)}), 500

@app.route('/watchlist', methods=['POST'])
def add_watchlist():
    try:
        data = request.get_json()
        if not data or not data.get('title'):
            return jsonify({"error": "Missing required field: title"}), 400
            
        title = data.get('title')
        year = data.get('year')
        poster = data.get('poster')
        
        # Check for duplicates using the helper function
        existing_movie = get_movie_by_title_db(title)
        if existing_movie:
            return jsonify({"error": "Movie already exists in watchlist"}), 409
            
        add_movie_db(title, year, poster)
        return jsonify({"message": "Movie added successfully"}), 201
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Failed to add movie", "details": str(e)}), 500

@app.route('/watchlist/<string:title>', methods=['DELETE'])
def delete_watchlist(title):
    try:
        existing_movie = get_movie_by_title_db(title)
        if not existing_movie:
            return jsonify({"error": "Movie not found in watchlist"}), 404
            
        delete_movie_db(title)
        return jsonify({"message": "Movie deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": "Failed to delete movie", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)