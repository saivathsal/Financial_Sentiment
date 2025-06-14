import bcrypt
import sqlite3
def get_connection():
    return sqlite3.connect("users.db", check_same_thread=False)

def create_user_table():
    with get_connection() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS users (
                        username TEXT PRIMARY KEY, 
                        password TEXT)''')

def add_user(username, password):
    try:
        with get_connection() as conn:
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                         (username, hash_password(password)))
        return True
    except sqlite3.IntegrityError:
        return False

def get_user(username):
    with get_connection() as conn:
        return conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())
