import sqlite3
import os

# Build the path to movies.db located in the backend folder
# os.path.dirname(__file__) gets the directory of this file
# '..' goes up one level to the backend directory where movies.db now lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '..', 'movies.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    # Allows us to access columns by name
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS watchlist 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                     title TEXT, year INTEGER)''')
    conn.commit()
    conn.close()

def get_watchlist_from_db():
    conn = get_db_connection()
    movies = conn.execute("SELECT title, year FROM watchlist").fetchall()
    conn.close()
    return [{"title": row["title"], "year": row["year"]} for row in movies]

def add_to_watchlist_db(title, year):
    conn = get_db_connection()
    conn.execute("INSERT INTO watchlist (title, year) VALUES (?, ?)", (title, year))
    conn.commit()
    conn.close()

def remove_from_watchlist_db(title):
    conn = get_db_connection()
    conn.execute("DELETE FROM watchlist WHERE title = ?", (title,))
    conn.commit()
    conn.close()