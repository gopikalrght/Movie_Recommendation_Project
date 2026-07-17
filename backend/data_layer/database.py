import sqlite3
import os

# Ensures the database is found even if run from different locations
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '..', '..', 'movies.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_watchlist_from_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM watchlist")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_movie_by_title_db(title):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM watchlist WHERE title = ?", (title,))
    movie = cursor.fetchone()
    conn.close()
    return dict(movie) if movie else None

def add_to_watchlist_db(title, year):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO watchlist (title, year) VALUES (?, ?)", (title, year))
    conn.commit()
    conn.close()

def remove_from_watchlist_db(title):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM watchlist WHERE title = ?", (title,))
    conn.commit()
    conn.close()