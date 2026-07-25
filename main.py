import mysql.connector

from database import connect_database


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
    """Search for hubs by location using a partial-match query."""
    location = input("Enter a location to search: ").strip()

    if not location:
        print("Location cannot be empty.")
        return

    connection = None

    try:
        connection = connect_database()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM hubs WHERE location LIKE %s"
        cursor.execute(query, (f"%{location}%",))
        hubs = cursor.fetchall()

        if not hubs:
            print("No hubs found for that location.")
            return

        print(f"\nFound {len(hubs)} hub(s):")
        display_hub_details(hubs)

    except mysql.connector.Error as exc:
        print(f"Database error: {exc}")

    finally:
        if connection is not None and connection.is_connected():
            connection.close()


def update_hub():
    """Update an existing hub after verifying that the hub ID exists."""
    hub_id_input = input("Enter Hub ID to update: ").strip()

    if not hub_id_input.isdigit():
        print("Invalid Hub ID. Please enter a number.")
        return

    hub_id = int(hub_id_input)
    connection = None

    try:
        connection = connect_database()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM hubs WHERE hub_id = %s", (hub_id,))
        hub = cursor.fetchone()

        if not hub:
            print("Hub not found.")
            return

        print("Current hub details:")
        display_hub_details([hub])

        updatable_columns = [column for column in hub.keys() if column != "hub_id"]
        updates = []
        values = []

        for column in updatable_columns:
            new_value = input(
                f"Enter new value for {column} (press Enter to keep current value): "
            ).strip()

            if new_value == "":
                continue

            if column.lower() == "capacity":
                if not new_value.isdigit():
                    print("Capacity must be a whole number.")
                    return

            updates.append(f"{column} = %s")
            values.append(new_value)

        if not updates:
            print("No changes were made.")
            return

        values.append(hub_id)
        query = f"UPDATE hubs SET {', '.join(updates)} WHERE hub_id = %s"
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


def delete_hub():
    """Delete an existing hub after confirmation from the user."""
    hub_id_input = input("Enter Hub ID to delete: ").strip()

    if not hub_id_input.isdigit():
        print("Invalid Hub ID. Please enter a number.")
        return

    hub_id = int(hub_id_input)
    connection = None

    try:
        connection = connect_database()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM hubs WHERE hub_id = %s", (hub_id,))
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

        cursor.execute("DELETE FROM hubs WHERE hub_id = %s", (hub_id,))
        connection.commit()
        print("Hub deleted successfully.")

    except mysql.connector.Error as exc:
        print(f"Database error: {exc}")

    finally:
        if connection is not None and connection.is_connected():
            connection.close()


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

        choice = input("Choose option: ").strip()

        if choice == "1":
            print("Register feature is not implemented in this branch.")
        elif choice == "2":
            print("Login feature is not implemented in this branch.")
        elif choice == "3":
            print("Add Hub feature is not implemented in this branch.")
        elif choice == "4":
            print("View Hubs feature is not implemented in this branch.")
        elif choice == "5":
            search_hub()
        elif choice == "6":
            update_hub()
        elif choice == "7":
            delete_hub()
        elif choice == "8":
            print("Thank you for using learning hub locator")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    menu()