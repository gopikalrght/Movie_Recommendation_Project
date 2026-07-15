import sqlite3
import os

# Path to backend/movies.db
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "backend", "movies.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Tables in database:", tables)

for table in tables:
    table_name = table[0]
    print(f"\nColumns for table '{table_name}':")

    cursor.execute(f"PRAGMA table_info('{table_name}')")
    columns = cursor.fetchall()

    for col in columns:
        print(f"- {col[1]} ({col[2]})")

conn.close()