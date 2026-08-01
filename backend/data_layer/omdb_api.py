import os
import requests
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

OMDB_API_KEY = os.getenv("OMDB_API_KEY")
OMDB_BASE_URL = "https://www.omdbapi.com/"


def search_movies(query):
    """
    Search OMDb for movies matching the user's query.
    Returns a list of search-result movies.
    """

    try:
        params = {
            "apikey": OMDB_API_KEY,
            "s": query,
            "type": "movie"
        }

        response = requests.get(
            OMDB_BASE_URL,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        if data.get("Response") == "False":
            return {
                "error": data.get(
                    "Error",
                    "Movie not found!"
                )
            }

        return data.get("Search", [])

    except requests.exceptions.RequestException as e:
        return {
            "error": str(e)
        }


def get_movie_details(imdb_id):
    """
    Get complete movie details using IMDb ID.
    """

    try:
        params = {
            "apikey": OMDB_API_KEY,
            "i": imdb_id,
            "plot": "full"
        }

        response = requests.get(
            OMDB_BASE_URL,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        if data.get("Response") == "False":
            return {
                "error": data.get(
                    "Error",
                    "Movie details not found!"
                )
            }

        return data

    except requests.exceptions.RequestException as e:
        return {
            "error": str(e)
        }