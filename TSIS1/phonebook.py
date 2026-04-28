import csv
import json
from pathlib import Path
from typing import Dict, List, Optional

from connect import connect, init_db

BASE_DIR = Path(__file__).resolve().parent
VALID_PHONE_TYPES = {"home", "work", "mobile"}

def parse_date(date_text: str):
    value = (date_text or "").strip()
    return value or None


def print_rows(rows):
    if not rows:
        print("No contacts found.")
        return

    print("\n" + "=" * 100)
    for row in rows:
        contact_id, name, email, birthday, group_name, phones, created_at = row
        print(f"ID: {contact_id}")
        print(f"Name: {name}")
        print(f"Email: {email or '-'}")
        print(f"Birthday: {birthday or '-'}")
        print(f"Group: {group_name or '-'}")
        print(f"Phones: {phones or '-'}")
        print(f"Created at: {created_at}")
        print("-" * 100)


def add_or_update_contact():
    print("\nAdd / update contact")
    name = input("Name: ").strip()
    email = input("Email: ").strip()
    birthday = parse_date(input("Birthday (YYYY-MM-DD or empty): "))
    group_name = input("Group [Family/Work/Friend/Other]: ").strip() or "Other"
    phone = input("Phone: ").strip()
    phone_type = input("Phone type [home/work/mobile]: ").strip().lower() or "mobile"

    try:
        with connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "CALL upsert_contact(%s, %s, %s, %s, %s, %s)",
                    (name, email or None, birthday, group_name, phone or None, phone_type),
                )
        print("Contact saved.")
    except Exception as e:
        print(f"Error: {e}")


def add_phone_to_existing_contact():
    print("\nAdd extra phone")
    name = input("Contact name: ").strip()
    phone = input("New phone: ").strip()
    phone_type = input("Type [home/work/mobile]: ").strip().lower() or "mobile"

    try:
        with connect() as conn:
            with conn.cursor() as cur:
                cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, phone_type))
        print("Phone added.")
    except Exception as e:
        print(f"Error: {e}")


def move_contact_to_group():
    print("\nMove contact to another group")
    name = input("Contact name: ").strip()
    group_name = input("New group: ").strip()

    try:
        with connect() as conn:
            with conn.cursor() as cur:
                cur.execute("CALL move_to_group(%s, %s)", (name, group_name))
        print("Contact moved.")
    except Exception as e:
        print(f"Error: {e}")


def search_all_fields():
    query = input("Search query (name/email/group/phone): ").strip()

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM search_contacts(%s)", (query,))
            rows = cur.fetchall()

    print_rows(rows)


def filter_by_group():
    group_name = input("Group name: ").strip()
    sort_by = input("Sort by [name/birthday/date]: ").strip().lower() or "name"

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM get_contacts_paginated(%s, %s, %s, %s, %s)",
                (1000, 0, group_name, None, sort_by),
            )
            rows = cur.fetchall()

    print_rows(rows)


def search_by_email():
    email_part = input("Email contains: ").strip()
    sort_by = input("Sort by [name/birthday/date]: ").strip().lower() or "name"

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM get_contacts_paginated(%s, %s, %s, %s, %s)",
                (1000, 0, None, email_part, sort_by),
            )
            rows = cur.fetchall()

    print_rows(rows)


def sorted_contacts():
    sort_by = input("Sort by [name/birthday/date]: ").strip().lower() or "name"

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM get_contacts_paginated(%s, %s, %s, %s, %s)",
                (1000, 0, None, None, sort_by),
            )
            rows = cur.fetchall()

    print_rows(rows)


def paginate_contacts():
    print("\nPaginated navigation")
    limit_value = int(input("Page size: ").strip() or "5")
    group_name = input("Filter by group (optional): ").strip() or None
    email_part = input("Search by email (optional): ").strip() or None
    sort_by = input("Sort by [name/birthday/date]: ").strip().lower() or "name"

    offset_value = 0

    while True:
        with connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM get_contacts_paginated(%s, %s, %s, %s, %s)",
                    (limit_value, offset_value, group_name, email_part, sort_by),
                )
                rows = cur.fetchall()

        print(f"\nPage offset = {offset_value}")
        print_rows(rows)

        command = input("Command [next / prev / quit]: ").strip().lower()
        if command == "next":
            if rows:
                offset_value += limit_value
            else:
                print("No more pages.")
        elif command == "prev":
            offset_value = max(0, offset_value - limit_value)
        elif command == "quit":
            break
        else:
            print("Unknown command.")


def fetch_contacts_as_json_ready() -> List[Dict]:
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    c.id,
                    c.name,
                    c.email,
                    c.birthday,
                    g.name,
                    c.created_at
                FROM contacts c
                LEFT JOIN groups g ON g.id = c.group_id
                ORDER BY c.name
                """
            )
            contacts = cur.fetchall()

            result = []
            for contact_id, name, email, birthday, group_name, created_at in contacts:
                cur.execute(
                    "SELECT phone, type FROM phones WHERE contact_id = %s ORDER BY id",
                    (contact_id,),
                )
                phones = cur.fetchall()
                result.append(
                    {
                        "name": name,
                        "email": email,
                        "birthday": str(birthday) if birthday else None,
                        "group": group_name,
                        "created_at": str(created_at),
                        "phones": [
                            {"phone": phone, "type": phone_type}
                            for phone, phone_type in phones
                        ],
                    }
                )
            return result


def export_to_json():
    file_name = input("JSON file name [contacts_export.json]: ").strip() or "contacts_export.json"
    file_path = BASE_DIR / file_name

    data = fetch_contacts_as_json_ready()
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"Exported to {file_path}")


def _save_contact_dict(cur, item: Dict, overwrite: bool):
    name = (item.get("name") or item.get("username") or "").strip()
    if not name:
        raise ValueError("Contact name is required")

    email = item.get("email")
    birthday = item.get("birthday")
    group_name = item.get("group") or item.get("group_name") or "Other"
    phones = item.get("phones") or []

    cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
    row = cur.fetchone()

    if row:
        contact_id = row[0]
        if overwrite:
            cur.execute(
                """
                INSERT INTO groups(name) VALUES (%s)
                ON CONFLICT (name) DO NOTHING
                """,
                (group_name,),
            )
            cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
            group_id = cur.fetchone()[0]
            cur.execute(
                "UPDATE contacts SET email = %s, birthday = %s, group_id = %s WHERE id = %s",
                (email, birthday, group_id, contact_id),
            )
            cur.execute("DELETE FROM phones WHERE contact_id = %s", (contact_id,))
        else:
            return
    else:
        first_phone = None
        first_type = "mobile"
        if phones:
            first_phone = phones[0].get("phone")
            first_type = phones[0].get("type") or "mobile"

        cur.execute(
            "CALL upsert_contact(%s, %s, %s, %s, %s, %s)",
            (name, email, birthday, group_name, first_phone, first_type),
        )
        cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
        contact_id = cur.fetchone()[0]
        phones = phones[1:] if first_phone else phones

    for phone_item in phones:
        phone = (phone_item.get("phone") or "").strip()
        phone_type = (phone_item.get("type") or "mobile").strip().lower()
        if not phone:
            continue
        if phone_type not in VALID_PHONE_TYPES:
            phone_type = "mobile"
        cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, phone_type))


def import_from_json():
    file_name = input("JSON file path: ").strip()
    file_path = Path(file_name)
    if not file_path.is_absolute():
        file_path = BASE_DIR / file_name

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    with connect() as conn:
        with conn.cursor() as cur:
            for item in data:
                name = (item.get("name") or item.get("username") or "").strip()
                if not name:
                    continue

                cur.execute("SELECT 1 FROM contacts WHERE name = %s", (name,))
                exists = cur.fetchone() is not None

                if exists:
                    decision = input(f"Duplicate contact '{name}'. [skip/overwrite]: ").strip().lower()
                    while decision not in {"skip", "overwrite"}:
                        decision = input("Please enter skip or overwrite: ").strip().lower()

                    if decision == "skip":
                        continue
                    _save_contact_dict(cur, item, overwrite=True)
                else:
                    _save_contact_dict(cur, item, overwrite=False)

    print("Import from JSON completed.")


def import_from_csv():
    file_name = input("CSV file path [contacts.csv]: ").strip() or "contacts.csv"
    file_path = Path(file_name)
    if not file_path.is_absolute():
        file_path = BASE_DIR / file_name

    grouped: Dict[str, Dict] = {}

    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Поддержка как нового формата CSV, так и старого username,phone
            name = (row.get("name") or row.get("username") or "").strip()
            if not name:
                continue

            email = (row.get("email") or "").strip() or None
            birthday = parse_date(row.get("birthday") or "")
            group_name = (row.get("group") or row.get("group_name") or "Other").strip() or "Other"
            phone = (row.get("phone") or "").strip()
            phone_type = (row.get("phone_type") or "mobile").strip().lower() or "mobile"
            if phone_type not in VALID_PHONE_TYPES:
                phone_type = "mobile"

            if name not in grouped:
                grouped[name] = {
                    "name": name,
                    "email": email,
                    "birthday": birthday,
                    "group": group_name,
                    "phones": [],
                }

            if phone:
                grouped[name]["phones"].append({"phone": phone, "type": phone_type})

    with connect() as conn:
        with conn.cursor() as cur:
            for item in grouped.values():
                try:
                    _save_contact_dict(cur, item, overwrite=True)
                except Exception as e:
                    print(f"Failed to import {item['name']}: {e}")

    print("CSV import completed.")


def delete_contact():
    print("1 - delete by name")
    print("2 - delete by phone")
    choice = input("Choice: ").strip()

    try:
        with connect() as conn:
            with conn.cursor() as cur:
                if choice == "1":
                    name = input("Contact name: ").strip()
                    cur.execute("CALL delete_contact(%s, %s)", (name, None))
                elif choice == "2":
                    phone = input("Phone: ").strip()
                    cur.execute("CALL delete_contact(%s, %s)", (None, phone))
                else:
                    print("Unknown choice.")
                    return
        print("Deleted.")
    except Exception as e:
        print(f"Error: {e}")


def menu():
    init_db()

    while True:
        print("\n===== Extended PhoneBook =====")
        print("1  - Add / update contact")
        print("2  - Add extra phone")
        print("3  - Search in all fields")
        print("4  - Filter by group")
        print("5  - Search by email")
        print("6  - Sort contacts")
        print("7  - Paginated navigation")
        print("8  - Export to JSON")
        print("9  - Import from JSON")
        print("10 - Import from CSV")
        print("11 - Move contact to group")
        print("12 - Delete contact")
        print("0  - Exit")

        choice = input("Choice: ").strip()

        if choice == "1":
            add_or_update_contact()
        elif choice == "2":
            add_phone_to_existing_contact()
        elif choice == "3":
            search_all_fields()
        elif choice == "4":
            filter_by_group()
        elif choice == "5":
            search_by_email()
        elif choice == "6":
            sorted_contacts()
        elif choice == "7":
            paginate_contacts()
        elif choice == "8":
            export_to_json()
        elif choice == "9":
            import_from_json()
        elif choice == "10":
            import_from_csv()
        elif choice == "11":
            move_contact_to_group()
        elif choice == "12":
            delete_contact()
        elif choice == "0":
            break
        else:
            print("Unknown menu item.")


if __name__ == "__main__":
    menu()
