"""
auth.py
Register & Login for admin users.

Implements:
    - register_admin() : creates a new admin account (username + hashed password)
    - login_admin()     : verifies username/password and returns the admin's id if correct

Uses connect_database() from database.py, matching this repo's setup.
Password hashing uses hashlib (sha256) - simple and dependency-free.
For production use, bcrypt/argon2 would be stronger, but this is fine
for a class prototype under time pressure.
"""

import hashlib
import mysql.connector

from database import connect_database


def hash_password(password):
    """Turn a plain-text password into a sha256 hash for storage."""
    return hashlib.sha256(password.encode()).hexdigest()


def register_admin():
    """
    Prompts for a new admin username and password, checks the username
    isn't already taken, then inserts the new admin into the 'admins' table.
    """
    print("\n--- Register New Admin ---")

    username = input("Choose a username: ").strip()
    password = input("Choose a password: ").strip()

    if not username or not password:
        print("Username and password cannot be empty.")
        return

    connection = None

    try:
        connection = connect_database()
        cursor = connection.cursor()

        # Check if username already exists
        cursor.execute("SELECT id FROM admins WHERE username = %s", (username,))
        existing = cursor.fetchone()

        if existing:
            print(f"Username '{username}' is already taken. Try a different one.")
            return

        password_hash = hash_password(password)

        cursor.execute(
            "INSERT INTO admins (username, password_hash) VALUES (%s, %s)",
            (username, password_hash)
        )
        connection.commit()
        print(f"\n✅ Admin '{username}' registered successfully (Admin ID: {cursor.lastrowid}).")

    except mysql.connector.Error as exc:
        print(f"Database error: {exc}")

    finally:
        if connection is not None and connection.is_connected():
            connection.close()


def login_admin():
    """
    Prompts for username and password, checks them against the 'admins' table.
    Returns the admin's id if login succeeds, otherwise None.
    """
    print("\n--- Admin Login ---")

    username = input("Username: ").strip()
    password = input("Password: ").strip()

    if not username or not password:
        print("Username and password cannot be empty.")
        return None

    connection = None

    try:
        connection = connect_database()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT id, password_hash FROM admins WHERE username = %s", (username,))
        admin = cursor.fetchone()

        if not admin:
            print("Invalid username or password.")
            return None

        password_hash = hash_password(password)

        if password_hash != admin["password_hash"]:
            print("Invalid username or password.")
            return None

        print(f"\n✅ Login successful. Welcome, {username}!")
        return admin["id"]

    except mysql.connector.Error as exc:
        print(f"Database error: {exc}")
        return None

    finally:
        if connection is not None and connection.is_connected():
            connection.close()