import sqlite3

def init_db():
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    # Ensure the table exists with both title and year
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS watchlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            year INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def add_to_watchlist(movie_data):
    # movie_data is the dictionary from server.py: {"title": "...", "year": ...}
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    
    # We use .get() so if 'year' is missing, it defaults to None/NULL
    title = movie_data.get('title')
    year = movie_data.get('year')
    
    cursor.execute("INSERT INTO watchlist (title, year) VALUES (?, ?)", (title, year))
    conn.commit()
    conn.close()

def get_watchlist():
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    cursor.execute("SELECT title, year FROM watchlist")
    rows = cursor.fetchall()
    conn.close()
    
    # Convert rows to a list of dictionaries for easier JSON response
    return [{"title": row[0], "year": row[1]} for row in rows]