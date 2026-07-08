import sqlite3

def get_db_connection():
    conn = sqlite3.connect('watchlist.db')
    return conn

def get_watchlist_from_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM watchlist")
    rows = cursor.fetchall()
    conn.close()
    return [{"title": row[0], "year": row[1]} for row in rows]

def add_to_watchlist_db(title, year):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Check for duplicates before adding
    cursor.execute("SELECT * FROM watchlist WHERE title = ?", (title,))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO watchlist (title, year) VALUES (?, ?)", (title, year))
        conn.commit()
    conn.close()

def remove_from_watchlist_db(title):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM watchlist WHERE title = ?", (title,))
    conn.commit()
    conn.close()