from flask import Flask, request, jsonify
from flask_cors import CORS
from .data_layer.tmdb_api import search_movies
from .data_layer.database import get_watchlist_from_db, add_to_watchlist_db, remove_from_watchlist_db

app = Flask(__name__)
CORS(app)

@app.route('/watchlist/get', methods=['GET'])
def get_watchlist():
    return jsonify(get_watchlist_from_db())

@app.route('/watchlist/add', methods=['POST'])
def add_watchlist():
    data = request.json
    add_to_watchlist_db(data['title'], data['year'])
    return jsonify({"message": "Success"})

@app.route('/watchlist/delete', methods=['POST'])
def delete_movie():
    data = request.json
    remove_from_watchlist_db(data['title'])
    return jsonify({"message": "Deleted"})

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    return jsonify(search_movies(query))

if __name__ == '__main__':
    app.run(debug=True)