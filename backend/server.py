from flask import Flask, request, jsonify
# 1. Import your function
from data_layer.tmdb_api import search_movies 

app = Flask(__name__)

# 2. Replace your old route with this clean version
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    # Use the function from your data_layer
    movies = search_movies(query) 
    return jsonify(movies)

if __name__ == '__main__':
    app.run(debug=True)