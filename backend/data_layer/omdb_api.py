import requests

# Replace with your actual OMDb API key
OMDB_API_KEY = "29edede1"
OMDB_BASE_URL = "http://www.omdbapi.com/"

def search_movies(query):
    """
    Searches for a movie using the OMDb API and returns complete movie details in JSON.
    """
    try:
        params = {
            "apikey": OMDB_API_KEY,
            "t": query
        }
        response = requests.get(OMDB_BASE_URL, params=params)
        
        # Check if response is successful
        if response.status_code == 401:
            return {"error": "Failed with status code 401"}
            
        data = response.json()
        
        # OMDb returns {"Response": "False", "Error": "Movie not found!"} if it fails
        if data.get("Response") == "False":
            return {"error": data.get("Error", "Movie not found")}
            
        return data

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}