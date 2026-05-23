import sqlite3
from tmdb_api import search_movies

connection = sqlite3.connect("movies.db")

cursor = connection.cursor()


# USERS TABLE

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
""")


# WATCHLIST TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS watchlist (
    watchlist_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    movie_title TEXT,
    imdb_id TEXT
)
""")

# ADD USER

def add_user(username, password):

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, password)
    )

    connection.commit()


# GET USERS

def get_users():

    cursor.execute("SELECT * FROM users")

    return cursor.fetchall()


# ADD TO WATCHLIST
def add_to_watchlist(username, movie_title, imdb_id):

    cursor.execute(
        "INSERT INTO watchlist (username, movie_title, imdb_id) VALUES (?, ?, ?)",
        (username, movie_title, imdb_id)
    )

    connection.commit()


# GET WATCHLIST
def get_watchlist(username):

    cursor.execute(
        "SELECT movie_title, imdb_id FROM watchlist WHERE username=?",
        (username,)
    )

    return cursor.fetchall()

def add_movie_from_api(username, movie_name):

    movies = search_movies(movie_name)

    if not movies:
        print("No movies found from API")
        return

    first_movie = movies[0]

    title = first_movie["title"]
    imdb_id = first_movie["imdb_id"]

    cursor.execute(
        "INSERT INTO watchlist (username, movie_title, imdb_id) VALUES (?, ?, ?)",
        (username, title, imdb_id)
    )

    connection.commit()


if __name__ == "__main__":
    add_movie_from_api("gopika", "Inception")
    print(get_watchlist("gopika"))
    connection.close()
