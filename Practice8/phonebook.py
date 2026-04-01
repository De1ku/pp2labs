from connect import connect, init_db, run_sql_file


def setup():
    init_db()
    run_sql_file("functions.sql")
    run_sql_file("procedures.sql")


def add_or_update_contact():
    username = input("username: ").strip()
    surname = input("surname: ").strip()
    phone = input("phone: ").strip()

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "CALL upsert_contact(%s, %s, %s)",
                (username, surname, phone)
            )

    print("done")


def search_contacts():
    pattern = input("pattern: ").strip()

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
            rows = cur.fetchall()

    for row in rows:
        print(row)


def paginate_contacts():
    limit_value = int(input("limit: "))
    offset_value = int(input("offset: "))

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM get_contacts_paginated(%s, %s)",
                (limit_value, offset_value)
            )
            rows = cur.fetchall()

    for row in rows:
        print(row)


def insert_many_contacts():
    usernames = [x.strip() for x in input("usernames (,): ").split(",")]
    surnames = [x.strip() for x in input("surnames (,): ").split(",")]
    phones = [x.strip() for x in input("phones (,): ").split(",")]

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "CALL insert_many_contacts(%s, %s, %s, %s)",
                (usernames, surnames, phones, "")
            )

            bad = ""
            if cur.description is not None:
                row = cur.fetchone()
                if row:
                    bad = row[0]

    if bad:
        print("incorrect data:", bad)
    else:
        print("all correct")


def delete_contact():
    print("1 - delete by username")
    print("2 - delete by phone")
    choice = input("choice: ").strip()

    with connect() as conn:
        with conn.cursor() as cur:
            if choice == "1":
                username = input("username: ").strip()
                cur.execute("CALL delete_contact(%s, %s)", (username, None))
            elif choice == "2":
                phone = input("phone: ").strip()
                cur.execute("CALL delete_contact(%s, %s)", (None, phone))

    print("deleted")


def menu():
    setup()

    while True:
        print("\n1 - add/update one contact")
        print("2 - search by pattern")
        print("3 - insert many contacts")
        print("4 - pagination")
        print("5 - delete")
        print("0 - exit")

        choice = input("choice: ").strip()

        if choice == "1":
            add_or_update_contact()
        elif choice == "2":
            search_contacts()
        elif choice == "3":
            insert_many_contacts()
        elif choice == "4":
            paginate_contacts()
        elif choice == "5":
            delete_contact()
        elif choice == "0":
            break


if __name__ == "__main__":
    menu()