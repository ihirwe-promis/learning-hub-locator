"""
hub_management.py
Member 3 - Add & View Hubs

Implements:
    - add_hub()   : inserts a new learning hub record into the 'hubs' table
    - view_hubs() : retrieves and displays all learning hub records

Uses connect_database() from database.py (MySQL connector), matching
this repo's actual setup.
"""

from database import connect_database


def add_hub(admin_id=None):
    """
    Prompts the admin for hub details and inserts a new row into
    the 'hubs' table using an SQL INSERT statement.

    admin_id: the id of the currently logged-in admin (from login_admin()).
              If None, the caller hasn't logged in - we block the action
              instead of silently using a placeholder id.
    """
    if admin_id is None:
        print("\nNope — log in as an admin first, then you can add a hub.")
        return

    print("\n--- Add a New Learning Hub ---")

    name = input("Hub name: ").strip()
    address = input("Address: ").strip()
    resources = input("Available resources (e.g. Wi-Fi, Books, Printer): ").strip()
    hours = input("Operating hours (e.g. Mon-Fri 8am-6pm): ").strip()
    contact = input("Contact info: ").strip()

    # Basic validation - don't allow empty required fields
    if not name or not address:
        print("Hold up — a hub needs at least a name and an address. Nothing was added.")
        return

    sync_status = "unsynced"   # new local record, not yet pushed/synced
    updated_by = admin_id       # real logged-in admin's id, no more hardcoding

    connection = None

    try:
        connection = connect_database()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO hubs (name, address, resources, hours, contact, sync_status, updated_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (name, address, resources, hours, contact, sync_status, updated_by)
        )
        connection.commit()
        print(f"\n✅ '{name}' was added successfully (Hub ID: {cursor.lastrowid}).")
    except Exception as error:
        print(f"\n❌ Failed to add hub: {error}")
    finally:
        if connection is not None and connection.is_connected():
            connection.close()


def view_hubs():
    """
    Retrieves all learning hub records from the 'hubs' table using an
    SQL SELECT statement and prints them in a readable format.
    """
    connection = None

    try:
        connection = connect_database()
        cursor = connection.cursor()

        cursor.execute("SELECT id, name, address, resources, hours, contact, sync_status FROM hubs")
        hubs = cursor.fetchall()

        if not hubs:
            print("\nNo learning hubs found in the database yet.")
            return

        print("\n--- Learning Hubs ---")
        for hub in hubs:
            hub_id, name, address, resources, hours, contact, sync_status = hub
            print(f"\nID: {hub_id}")
            print(f"Name: {name}")
            print(f"Address: {address}")
            print(f"Resources: {resources}")
            print(f"Hours: {hours}")
            print(f"Contact: {contact}")
            print(f"Sync status: {sync_status}")
        print()

    except Exception as error:
        print(f"\n❌ Failed to retrieve hubs: {error}")
    finally:
        if connection is not None and connection.is_connected():
            connection.close()


# Manual test block - run this file directly to test your two functions
# without needing the full menu system.
if __name__ == "__main__":
    while True:
        print("\n1. Add Hub\n2. View Hubs\n3. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_hub()
        elif choice == "2":
            view_hubs()
        elif choice == "3":
            break
        else:
            print("Invalid option, try again.")
            