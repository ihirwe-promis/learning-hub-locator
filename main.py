import mysql.connector

from database import connect_database
from hub_management import add_hub, view_hubs
from auth import register_admin, login_admin


def display_hub_details(hubs):
    if not hubs:
        print("No hub records found.")
        return

    for hub in hubs:
        print("\nHub Details:")
        for key, value in hub.items():
            print(f"{key}: {value}")
        print("-" * 25)


def search_hub():
    """Search for hubs by address using a partial-match query."""
    address = input("Enter an address to search: ").strip()

    if not address:
        print("Address cannot be empty.")
        return

    connection = None

    try:
        connection = connect_database()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM hubs WHERE address LIKE %s"
        cursor.execute(query, (f"%{address}%",))
        hubs = cursor.fetchall()

        if not hubs:
            print("No hubs found for that address.")
            return

        print(f"\nFound {len(hubs)} hub(s):")
        display_hub_details(hubs)

    except mysql.connector.Error as exc:
        print(f"Database error: {exc}")

    finally:
        if connection is not None and connection.is_connected():
            connection.close()


def update_hub(admin_id=None):
    """Update an existing hub after verifying that the hub ID exists."""
    if admin_id is None:
        print("\nYou must be logged in as an admin to update a hub.")
        return

    hub_id_input = input("Enter Hub ID to update: ").strip()

    if not hub_id_input.isdigit():
        print("Invalid Hub ID. Please enter a number.")
        return

    hub_id = int(hub_id_input)
    connection = None

    try:
        connection = connect_database()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM hubs WHERE id = %s", (hub_id,))
        hub = cursor.fetchone()

        if not hub:
            print("Hub not found.")
            return

        print("Current hub details:")
        display_hub_details([hub])

        updatable_columns = [column for column in hub.keys() if column not in ("id", "updated_by")]
        updates = []
        values = []

        for column in updatable_columns:
            new_value = input(
                f"Enter new value for {column} (press Enter to keep current value): "
            ).strip()

            if new_value == "":
                continue

            updates.append(f"{column} = %s")
            values.append(new_value)

        if not updates:
            print("No changes were made.")
            return

        values.append(hub_id)
        query = f"UPDATE hubs SET {', '.join(updates)} WHERE id = %s"
        cursor.execute(query, tuple(values))
        connection.commit()
        print("Hub updated successfully.")

    except ValueError as exc:
        print(exc)

    except mysql.connector.Error as exc:
        print(f"Database error: {exc}")

    finally:
        if connection is not None and connection.is_connected():
            connection.close()


def delete_hub(admin_id=None):
    """Delete an existing hub after confirmation from the user."""
    if admin_id is None:
        print("\nYou must be logged in as an admin to delete a hub.")
        return

    hub_id_input = input("Enter Hub ID to delete: ").strip()

    if not hub_id_input.isdigit():
        print("Invalid Hub ID. Please enter a number.")
        return

    hub_id = int(hub_id_input)
    connection = None

    try:
        connection = connect_database()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM hubs WHERE id = %s", (hub_id,))
        hub = cursor.fetchone()

        if not hub:
            print("Hub not found.")
            return

        print("Hub to delete:")
        display_hub_details([hub])

        confirmation = input("Are you sure you want to delete this hub? (y/n): ").strip().lower()
        if confirmation not in {"y", "yes"}:
            print("Delete cancelled.")
            return

        cursor.execute("DELETE FROM hubs WHERE id = %s", (hub_id,))
        connection.commit()
        print("Hub deleted successfully.")

    except mysql.connector.Error as exc:
        print(f"Database error: {exc}")

    finally:
        if connection is not None and connection.is_connected():
            connection.close()


def menu():
    logged_in_admin_id = None  # tracks which admin is currently logged in, if any

    while True:
        status = f"Logged in as admin #{logged_in_admin_id}" if logged_in_admin_id else "Not logged in"
        print(f"""
[{status}]
1. Register
2. Login
3. Add Hub
4. View Hubs
5. Search Hub
6. Update Hub
7. Delete Hub
8. Exit
""")

        choice = input("Choose option: ").strip()

        if choice == "1":
            register_admin()
        elif choice == "2":
            admin_id = login_admin()
            if admin_id is not None:
                logged_in_admin_id = admin_id
        elif choice == "3":
            add_hub(logged_in_admin_id)
        elif choice == "4":
            view_hubs()
        elif choice == "5":
            search_hub()
        elif choice == "6":
            update_hub(logged_in_admin_id)
        elif choice == "7":
            delete_hub(logged_in_admin_id)
        elif choice == "8":
            print("Thank you for using learning hub locator")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    menu()
    