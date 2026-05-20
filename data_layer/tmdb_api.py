movies = [
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

def search_movie(movie_name):
    
    results = []

    for movie in movies:

        if movie_name.lower() in movie["title"].lower():

            results.append(movie)

    return results


print(search_movie("inter"))