import sqlite3

def init_db():
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS watchlist 
                      (id INTEGER PRIMARY KEY, title TEXT, year TEXT)''')
    conn.commit()
    conn.close()

def add_to_watchlist(movie_data):
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO watchlist (title, year) VALUES (?, ?)", 
                   (movie_data['title'], movie_data['year']))
    conn.commit()
    conn.close()

def get_watchlist():
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM watchlist")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "title": r[1], "year": r[2]} for r in rows]