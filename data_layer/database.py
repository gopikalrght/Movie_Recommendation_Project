import sqlite3

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
    movie_title TEXT
)
""")


# ADD USER

def add_user(username, password):

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, password)
    )

    connection.commit()

    print("User added successfully")


# GET USERS

def get_users():

    cursor.execute("SELECT * FROM users")

    return cursor.fetchall()


# ADD TO WATCHLIST

def add_to_watchlist(username, movie_title):

    cursor.execute(
        "INSERT INTO watchlist (username, movie_title) VALUES (?, ?)",
        (username, movie_title)
    )

    connection.commit()

    print("Movie added to watchlist")


# GET WATCHLIST

def get_watchlist():

    cursor.execute("SELECT * FROM watchlist")

    return cursor.fetchall()


add_to_watchlist("gopika", "Interstellar")

print(get_watchlist())

connection.close()