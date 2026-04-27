CREATE TABLE IF NOT EXISTS groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS contacts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(100),
    birthday DATE,
    group_id INTEGER REFERENCES groups(id) ON DELETE SET NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS phones (
    id SERIAL PRIMARY KEY,
    contact_id INTEGER NOT NULL REFERENCES contacts(id) ON DELETE CASCADE,
    phone VARCHAR(20) NOT NULL UNIQUE,
    type VARCHAR(10) NOT NULL CHECK (type IN ('home', 'work', 'mobile')),
    UNIQUE(contact_id, phone)
);

INSERT INTO groups(name)
VALUES ('Family'), ('Work'), ('Friend'), ('Other')
ON CONFLICT (name) DO NOTHING;

CREATE INDEX IF NOT EXISTS idx_contacts_name ON contacts (LOWER(name));
CREATE INDEX IF NOT EXISTS idx_contacts_email ON contacts (LOWER(email));
CREATE INDEX IF NOT EXISTS idx_contacts_birthday ON contacts (birthday);
CREATE INDEX IF NOT EXISTS idx_contacts_created_at ON contacts (created_at);
CREATE INDEX IF NOT EXISTS idx_phones_phone ON phones (phone);

-- ---------------------------------
-- Мягкая миграция со старой таблицы phonebook
-- ---------------------------------
DO $$
DECLARE
    has_phonebook BOOLEAN;
    has_surname BOOLEAN;
    other_group_id INTEGER;
BEGIN
    SELECT EXISTS (
        SELECT 1
        FROM information_schema.tables
        WHERE table_schema = 'public' AND table_name = 'phonebook'
    ) INTO has_phonebook;

    IF has_phonebook THEN
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.columns
            WHERE table_schema = 'public'
              AND table_name = 'phonebook'
              AND column_name = 'surname'
        ) INTO has_surname;

        SELECT id INTO other_group_id FROM groups WHERE name = 'Other';

        IF has_surname THEN
            INSERT INTO contacts(name, group_id)
            SELECT DISTINCT
                TRIM(CONCAT(username, CASE WHEN COALESCE(surname, '') <> '' THEN ' ' || surname ELSE '' END)),
                other_group_id
            FROM phonebook
            ON CONFLICT (name) DO NOTHING;

            INSERT INTO phones(contact_id, phone, type)
            SELECT c.id, pb.phone, 'mobile'
            FROM phonebook pb
            JOIN contacts c
              ON c.name = TRIM(CONCAT(pb.username, CASE WHEN COALESCE(pb.surname, '') <> '' THEN ' ' || pb.surname ELSE '' END))
            ON CONFLICT (phone) DO NOTHING;
        ELSE
            INSERT INTO contacts(name, group_id)
            SELECT DISTINCT username, other_group_id
            FROM phonebook
            ON CONFLICT (name) DO NOTHING;

            INSERT INTO phones(contact_id, phone, type)
            SELECT c.id, pb.phone, 'mobile'
            FROM phonebook pb
            JOIN contacts c ON c.name = pb.username
            ON CONFLICT (phone) DO NOTHING;
        END IF;
    END IF;
END $$;
