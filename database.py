import mysql.connector
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()


def connect_database():
    connection = mysql.connector.connect(
        host="mysql-267997fe-alustudent-08b3.a.aivencloud.com",
        user="avnadmin",
        port=19949,
        password=os.environ.get("DB_PASSWORD"),
        database="learning_hub"
    )
    return connection
def create_users_table():
    """Creates the users table if it doesn't already exist."""
    connection = connect_database()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL
        )
    """)
    connection.commit()
    cursor.close()
    connection.close()


def register_user(username, password):
    """Registers a new user with a hashed password. Returns True on success."""
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    if cursor.fetchone():
        print("This username is already taken. Please choose another one.")
        cursor.close()
        connection.close()
        return False

    password_hash = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute(
        "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
        (username, password_hash)
    )
    connection.commit()
    cursor.close()
    connection.close()
    print(f"User '{username}' registered successfully!")
    return True


def login(username, password):
    """Validates login credentials. Returns True if login succeeds, False otherwise."""
    connection = connect_database()
    cursor = connection.cursor()

    password_hash = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute(
        "SELECT id FROM users WHERE username = %s AND password_hash = %s",
        (username, password_hash)
    )
    user = cursor.fetchone()
    cursor.close()
    connection.close()

    if user:
        print(f"Welcome back, {username}!")
        return True
    else:
        print("Invalid username or password. Please try again.")
        return False
