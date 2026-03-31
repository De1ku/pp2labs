import csv
from connect import connect, init_db


def insert_from_csv(filename):
    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        with connect() as conn:
            with conn.cursor() as cur:
                for row in reader:
                    cur.execute("""
                        INSERT INTO phonebook (username, phone)
                        VALUES (%s, %s)
                        ON CONFLICT (username)
                        DO UPDATE SET phone = EXCLUDED.phone
                    """, (row["username"], row["phone"]))

    print("CSV loaded")


def insert_from_console():
    username = input("username: ")
    phone = input("phone: ")

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO phonebook (username, phone) VALUES (%s, %s)",
                (username, phone)
            )

    print("Contact added")


def update_contact():
    print("1 - update username")
    print("2 - update phone")
    choice = input("choice: ")

    with connect() as conn:
        with conn.cursor() as cur:
            if choice == "1":
                old_name = input("old username: ")
                new_name = input("new username: ")
                cur.execute(
                    "UPDATE phonebook SET username = %s WHERE username = %s",
                    (new_name, old_name)
                )
            elif choice == "2":
                name = input("username: ")
                new_phone = input("new phone: ")
                cur.execute(
                    "UPDATE phonebook SET phone = %s WHERE username = %s",
                    (new_phone, name)
                )

    print("Updated")


def query_contacts():
    print("1 - show all")
    print("2 - search by name")
    print("3 - search by phone prefix")
    choice = input("choice: ")

    with connect() as conn:
        with conn.cursor() as cur:
            if choice == "1":
                cur.execute("SELECT * FROM phonebook ORDER BY id")
            elif choice == "2":
                name = input("name: ")
                cur.execute(
                    "SELECT * FROM phonebook WHERE username LIKE %s",
                    (f"%{name}%",)
                )
            elif choice == "3":
                prefix = input("prefix: ")
                cur.execute(
                    "SELECT * FROM phonebook WHERE phone LIKE %s",
                    (f"{prefix}%",)
                )
            else:
                return

            rows = cur.fetchall()

    for row in rows:
        print(row)


def delete_contact():
    print("1 - delete by username")
    print("2 - delete by phone")
    choice = input("choice: ")

    with connect() as conn:
        with conn.cursor() as cur:
            if choice == "1":
                name = input("username: ")
                cur.execute("DELETE FROM phonebook WHERE username = %s", (name,))
            elif choice == "2":
                phone = input("phone: ")
                cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))

    print("Deleted")


def menu():
    init_db()

    while True:
        print("\n1 - insert from csv")
        print("2 - insert from console")
        print("3 - update")
        print("4 - query")
        print("5 - delete")
        print("0 - exit")

        choice = input("choice: ")

        if choice == "1":
            insert_from_csv("contacts.csv")
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            update_contact()
        elif choice == "4":
            query_contacts()
        elif choice == "5":
            delete_contact()
        elif choice == "0":
            break


menu()