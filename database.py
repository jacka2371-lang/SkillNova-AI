
import sqlite3
import bcrypt

from pathlib import Path

DATABASE_NAME = Path(__file__).resolve().parent / "resume_ai.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    # Table for registered users
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash BLOB NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Table for each user's saved resume analyses
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analysis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            job_title TEXT NOT NULL,
            results_json TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    connection.commit()
    connection.close()


def register_user(name, email, password):
    name = name.strip()
    email = email.strip().lower()

    if not name or not email or not password:
        return False, "Please fill in all fields."

    if len(password) < 8:
        return False, "Password must contain at least 8 characters."

    if len(password.encode("utf-8")) > 72:
        return False, "Password must not exceed 72 UTF-8 bytes."

    password_hash = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO users (name, email, password_hash)
            VALUES (?, ?, ?)
        """, (name, email, password_hash))

        connection.commit()
        return True, "Account created successfully!"

    except sqlite3.IntegrityError:
        return False, "This email is already registered."

    finally:
        connection.close()


def authenticate_user(email, password):
    email = email.strip().lower()

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT id, name, email, password_hash
            FROM users
            WHERE email = ?
        """, (email,))

        user = cursor.fetchone()

        if user is None:
            return None

        stored_hash = user["password_hash"]

        if bcrypt.checkpw(
            password.encode("utf-8"),
            stored_hash
        ):
            return {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"]
            }

        return None

    finally:
        connection.close()


def save_analysis(user_id, job_title, results_json):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO analysis_history
                (user_id, job_title, results_json)
            VALUES (?, ?, ?)
        """, (user_id, job_title, results_json))

        connection.commit()

    finally:
        connection.close()


def get_user_history(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT id, job_title, results_json, created_at
            FROM analysis_history
            WHERE user_id = ?
            ORDER BY created_at DESC
        """, (user_id,))

        return [dict(row) for row in cursor.fetchall()]

    finally:
        connection.close()


# Create the tables when this module is initialized.
create_tables()
