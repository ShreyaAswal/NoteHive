import sqlite3
import hashlib # To hash passwords for security
import os

def get_db_connection():
    # Get the absolute path to the directory where this script is located (the backend folder)
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    # Join that path with the desired database filename
    db_path = os.path.join(backend_dir, 'notehive.db')
    
    # Connect to the database using the full, absolute path
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# Function to create the users table if it doesn't exist
def create_users_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Function to hash a password
def hash_password(password):
    # Salting passwords before hashing is a best practice, but for simplicity we'll hash directly
    return hashlib.sha256(password.encode()).hexdigest()

# Function to add a new user to the database
def add_user(username, email, password):
    """Adds a new user to the database with a hashed password."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Hash the password before storing it
    hashed_password = hash_password(password)
    
    try:
        cursor.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            (username, email, hashed_password)
        )
        conn.commit()
        return True, "User created successfully."
    except sqlite3.IntegrityError as e:
        # This error occurs if the username or email is already taken (due to UNIQUE constraint)
        if 'UNIQUE constraint failed: users.username' in str(e):
            return False, "Username already exists. Please choose another."
        elif 'UNIQUE constraint failed: users.email' in str(e):
            return False, "Email is already registered. Please log in."
        else:
            return False, "An error occurred."
    finally:
        conn.close()

#for login a user    
def verify_user(username_or_email, password):
    """
    Verifies user credentials. On success, returns True and the user's data.
    On failure, returns False and an error message.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_password_to_check = hash_password(password)
    
    cursor.execute(
        "SELECT * FROM users WHERE username = ? OR email = ?",
        (username_or_email, username_or_email)
    )
    user = cursor.fetchone()
    conn.close()
    
    if user and user['password_hash'] == hashed_password_to_check:
        # Success: Return True and the user's data as a dictionary
        return True, dict(user)
    elif user:
        return False, "Incorrect password. Please try again."
    else:
        return False, "User not found. Please check your username or email."

# --- INITIAL SETUP ---
# This function call will run once when the app starts, ensuring the table is ready.
create_users_table()
