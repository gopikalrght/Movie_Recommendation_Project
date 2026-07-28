import requests
import os

# You can replace this with your actual OMDb API key if needed
OMDB_API_KEY = os.getenv("OMDB_API_KEY", "29edede1")

def search_movies(query):
    url = f"https://www.omdbapi.com/?apikey={OMDB_API_KEY}&s={query}"
    response = requests.get(url)
    
    if response.status_code != 200:
        return {"error": "Failed to connect to OMDb API"}, 500
        
    data = response.json()
    if data.get("Response") == "True":
        return data.get("Search", []), 200
    else:
        return {"error": data.get("Error", "Movies not found")}, 404

def get_movie_details(imdb_id):
    url = f"https://www.omdbapi.com/?apikey={OMDB_API_KEY}&i={imdb_id}"
    response = requests.get(url)
    
    if response.status_code != 200:
        return {"error": "Failed to connect to OMDb API"}, 500
        
    data = response.json()
    if data.get("Response") == "True":
        return data, 200
    else:
        return {"error": data.get("Error", "Movie details not found")}, 404