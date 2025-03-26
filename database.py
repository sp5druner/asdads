import sqlite3
from config import DATABASE_FILE

def init_db():
    with sqlite3.connect(DATABASE_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS allowed_users (
                user_id INTEGER PRIMARY KEY
            )
        """)

def get_allowed_users():
    with sqlite3.connect(DATABASE_FILE) as conn:
        users = conn.execute("SELECT user_id FROM allowed_users").fetchall()
    return {user[0] for user in users}

def add_allowed_user(user_id):
    with sqlite3.connect(DATABASE_FILE) as conn:
        conn.execute("INSERT OR IGNORE INTO allowed_users (user_id) VALUES (?)", (user_id,))

def remove_allowed_user(user_id):
    with sqlite3.connect(DATABASE_FILE) as conn:
        conn.execute("DELETE FROM allowed_users WHERE user_id = ?", (user_id,))
