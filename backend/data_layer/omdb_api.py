import requests
import os

OMDB_API_KEY = "your_omdb_api_key_here"  # Make sure this is your active OMDb API key

def search_movies(query):
    # Using 't' parameter for precise title matching or switch to 's' if handling lists, 
    # but 't' returns the detailed dictionary requested.
    url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={query}"
    response = requests.get(url)
    
    if response.status_code != 200:
        return {"error": "Failed to connect to OMDb API"}
    
    data = response.json()
    
    if data.get("Response") == "False":
        return {"error": data.get("Error", "Movie not found")}
        
    # Return complete JSON containing all requested fields
    return {
        "title": data.get("Title"),
        "year": data.get("Year"),
        "poster": data.get("Poster"),
        "plot": data.get("Plot"),
        "imdb_rating": data.get("imdbRating"),
        "genre": data.get("Genre"),
        "director": data.get("Director"),
        "actors": data.get("Actors")
    }