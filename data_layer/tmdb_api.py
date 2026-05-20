import requests

API_KEY = "1204abf9d5acbc28450fc50bc1566b43"


fallback_movies = [
    {
        "movie_id": 1,
        "title": "Avatar",
        "rating": 8.2,
        "genre": "Sci-Fi"
    },
    {
        "movie_id": 2,
        "title": "Interstellar",
        "rating": 8.6,
        "genre": "Sci-Fi"
    },
    {
        "movie_id": 3,
        "title": "Titanic",
        "rating": 7.9,
        "genre": "Romance"
    }
]


def get_popular_movies():

    url = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}"

    try:

        response = requests.get(url, timeout=10)

        data = response.json()

        movies = []

        for movie in data["results"]:

            movies.append({
                "title": movie["title"],
                "rating": movie["vote_average"]
            })

        print("Live TMDB data loaded")

        return movies

    except:

        print("TMDB failed — using fallback local data")

        return fallback_movies


print(get_popular_movies())