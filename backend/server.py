
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# The list to store watchlist items
watchlist = []

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    # Make sure to replace YOUR_API_KEY_HERE with your real TMDB key
    api_key = '444b3df3d5964569d69a05e7090c6b64'
    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={query}"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        return jsonify(data.get('results', []))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/watchlist/add', methods=['POST'])
def add_to_watchlist():
    data = request.json
    watchlist.append(data)
    return jsonify({"message": "Added to watchlist!"})

@app.route('/watchlist/get', methods=['GET'])
def get_watchlist():
    return jsonify(watchlist)

if __name__ == '__main__':
    app.run(port=5000)