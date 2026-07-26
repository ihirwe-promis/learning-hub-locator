from database import connect_database
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

        if choice == "3":
            add_hub()
        elif choice == "4":
            view_hubs()
        elif choice == "8":
            print("Thank you for using learning hub locator")
            break