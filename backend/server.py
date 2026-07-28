from flask import Flask, jsonify, request
from flask_cors import CORS
from backend.data_layer.omdb_api import search_movies, get_movie_details

app = Flask(__name__)
CORS(app)

watchlist_db = []

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400
    
    result, status_code = search_movies(query)
    return jsonify(result), status_code

@app.route("/movie/<imdb_id>", methods=["GET"])
def movie_details(imdb_id):
    result, status_code = get_movie_details(imdb_id)
    return jsonify(result), status_code

@app.route("/recommend", methods=["GET"])
def recommend():
    title = request.args.get("title")
    imdb_id = request.args.get("imdbID")
    
    query_term = title
    if imdb_id and not query_term:
        details, status = get_movie_details(imdb_id)
        if status == 200:
            query_term = details.get("Title")
            
    if not query_term:
        return jsonify({"error": "Title or imdbID parameter is required for recommendations"}), 400
        
    movies, status_code = search_movies(query_term)
    if status_code != 200:
        return jsonify(movies), status_code
        
    recommendations = []
    for m in movies[:10]:
        recommendations.append({
            "Title": m.get("Title"),
            "Year": m.get("Year"),
            "Poster": m.get("Poster"),
            "imdbID": m.get("imdbID")
        })
        
    return jsonify(recommendations), 200

@app.route("/watchlist", methods=["GET"])
def get_watchlist():
    return jsonify(watchlist_db), 200

@app.route("/watchlist", methods=["POST"])
def add_to_watchlist():
    data = request.get_json()
    if not data or "imdbID" not in data:
        return jsonify({"error": "Invalid payload, imdbID required"}), 400
        
    for item in watchlist_db:
        if item.get("imdbID") == data.get("imdbID"):
            return jsonify({"message": "Movie already in watchlist"}), 200
            
    watchlist_item = {
        "imdbID": data.get("imdbID"),
        "title": data.get("title") or data.get("Title"),
        "year": data.get("year") or data.get("Year"),
        "poster": data.get("poster") or data.get("Poster")
    }
    
    watchlist_db.append(watchlist_item)
    return jsonify({"message": "Added to watchlist successfully", "item": watchlist_item}), 201

@app.route("/watchlist/<imdb_id>", methods=["DELETE"])
def delete_from_watchlist(imdb_id):
    global watchlist_db
    initial_length = len(watchlist_db)
    watchlist_db = [item for item in watchlist_db if item.get("imdbID") != imdb_id]
    
    if len(watchlist_db) < initial_length:
        return jsonify({"message": "Removed from watchlist successfully"}), 200
    return jsonify({"error": "Movie not found in watchlist"}), 404

if __name__ == "__main__":
    app.run(debug=True, port=5000)