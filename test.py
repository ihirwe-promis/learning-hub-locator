from database import connect_database

connection = connect_database()

if connection.is_connected():
    print("Database connected successfully!")

connection.close()