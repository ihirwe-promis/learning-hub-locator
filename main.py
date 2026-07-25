from database import connect_database

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

        # Features will be added here

        if choice == "8":
            print("Thank you for using learning hub locator")


menu()