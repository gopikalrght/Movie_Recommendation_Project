import requests

API_KEY ="78cdf749"

# 1. SEARCH MOVIES (by name)
def search_movies(movie_name):

    try:
        url = f"http://www.omdbapi.com/?apikey={API_KEY}&s={movie_name}"

        response = requests.get(url, timeout=10)
        data = response.json()

        movies = []

        if data.get("Response") == "True":

            for item in data.get("Search", []):

                movies.append({
                    "title": item.get("Title"),
                    "year": item.get("Year"),
                    "imdb_id": item.get("imdbID"),
                    "poster": item.get("Poster")
                })

        return movies

    except Exception as e:
        print("Search Error:", e)
        return []


# 2. GET FULL MOVIE DETAILS (by imdb_id)
def get_movie_details(imdb_id):

    try:
        url = f"http://www.omdbapi.com/?apikey={API_KEY}&i={imdb_id}"

        response = requests.get(url, timeout=10)
        data = response.json()

        return {
            "title": data.get("Title"),
            "year": data.get("Year"),
            "genre": data.get("Genre"),
            "rating": data.get("imdbRating"),
            "plot": data.get("Plot"),
            "actors": data.get("Actors"),
            "poster": data.get("Poster")
        }

    except Exception as e:
        print("Details Error:", e)
        return {}

if __name__ == "__main__":

    movies = search_movies("Batman")

    if movies:

        first_id = movies[0]["imdb_id"]

        print(get_movie_details(first_id))

    else:

        print("No movies found or API failed")