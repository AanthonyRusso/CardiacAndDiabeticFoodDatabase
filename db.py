import sqlite3

DB_NAME = "food.db"

def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    con = get_connection()
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS Food (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT,
        carbs REAL,
        GI REAL,
        GINote TEXT,
        sodium REAL,
        SodiumStatus TEXT,
        calories REAL,
        ServingSize TEXT
    )
    """)

    con.commit()
    con.close()