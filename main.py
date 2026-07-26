from database import connect_database, register_user, login, create_users_table
from hub_management import add_hub, view_hubs


def menu():
    while True:
        print("""
1. Register
2. Login
3. Add Hub
4. View Hubs
5. Search Hub
6. Update Hub
7. Delete Hub
8. Exit
""")
        choice = input("Choose option: ")

        if choice == "1":
            username = input("Choose a username: ")
            password = input("Choose a password: ")
            register_user(username, password)

        elif choice == "2":
            username = input("Username: ")
            password = input("Password: ")
            login(username, password)

        # Features will be added here

        elif choice == "8":
            print("Thank you for using learning hub locator")
            break


create_users_table()
menu()