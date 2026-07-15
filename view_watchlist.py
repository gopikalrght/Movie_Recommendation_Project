import sqlite3
import os

# Path to backend/movies.db
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "backend", "movies.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("SELECT * FROM watchlist")
rows = cursor.fetchall()

print("Watchlist data:")
for row in rows:
    print(row)

conn.close()