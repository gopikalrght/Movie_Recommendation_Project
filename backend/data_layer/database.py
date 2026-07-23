import sqlite3
import os

# Define absolute path for the database to ensure it points to the right place
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '..', 'movies.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS watchlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            year TEXT,
            poster TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_watchlist_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM watchlist')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_movie_by_title_db(title):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM watchlist WHERE title = ?', (title,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def add_movie_db(title, year, poster):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO watchlist (title, year, poster) VALUES (?, ?, ?)', (title, year, poster))
    conn.commit()
    conn.close()

def delete_movie_db(title):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM watchlist WHERE title = ?', (title,))
    conn.commit()
    conn.close()