import requests
import os

OMDB_API_KEY = "444b3df3d5964569d69a05e7090c6b64" # Your real OMDb API key

def search_movies(query):
    # Using https:// instead of http:// and adding a timeout
    url = f"https://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={query}"
    
    try:
        response = requests.get(url, timeout=5)
        
        if response.status_code != 200:
            return {"error": f"Failed with status code {response.status_code}"}
        
        data = response.json()
        
        if data.get("Response") == "False":
            return {"error": data.get("Error", "Movie not found")}
            
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
    except requests.exceptions.RequestException as e:
        return {"error": f"Connection exception: {str(e)}"}