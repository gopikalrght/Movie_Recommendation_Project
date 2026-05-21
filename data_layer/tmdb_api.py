import requests

API_KEY = "78cdf749"


def search_movie(movie_name):

    url = f"http://www.omdbapi.com/?apikey={API_KEY}&t={movie_name}"

    response = requests.get(url)

    data = response.json()

    movie = {
        "title": data.get("Title"),
        "year": data.get("Year"),
        "genre": data.get("Genre"),
        "rating": data.get("imdbRating"),
        "poster":data.get("Poster")
    }
    return movie