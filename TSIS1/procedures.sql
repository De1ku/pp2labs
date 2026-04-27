DROP PROCEDURE IF EXISTS upsert_contact(VARCHAR, VARCHAR, VARCHAR);
DROP PROCEDURE IF EXISTS upsert_contact(VARCHAR, VARCHAR, DATE, VARCHAR, VARCHAR, VARCHAR);

DROP PROCEDURE IF EXISTS insert_many_contacts(TEXT[], TEXT[], TEXT[], TEXT);

DROP PROCEDURE IF EXISTS delete_contact(VARCHAR, VARCHAR);

DROP PROCEDURE IF EXISTS add_phone(VARCHAR, VARCHAR, VARCHAR);
DROP PROCEDURE IF EXISTS move_to_group(VARCHAR, VARCHAR);


CREATE OR REPLACE PROCEDURE upsert_contact(
    p_name VARCHAR,
    p_email VARCHAR,
    p_birthday DATE,
    p_group_name VARCHAR,
    p_phone VARCHAR,
    p_phone_type VARCHAR DEFAULT 'mobile'
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INT;
    v_group_id INT;
    v_existing_contact_id INT;
BEGIN
    IF p_name IS NULL OR TRIM(p_name) = '' THEN
        RAISE EXCEPTION 'Contact name cannot be empty';
    END IF;

    IF p_phone IS NOT NULL AND TRIM(p_phone) <> '' AND p_phone !~ '^\+?[0-9]{10,15}$' THEN
        RAISE EXCEPTION 'Incorrect phone: %', p_phone;
    END IF;

    IF p_phone_type IS NOT NULL AND p_phone_type NOT IN ('home', 'work', 'mobile') THEN
        RAISE EXCEPTION 'Incorrect phone type: %', p_phone_type;
    END IF;

    IF p_group_name IS NULL OR TRIM(p_group_name) = '' THEN
        p_group_name := 'Other';
    END IF;

    INSERT INTO groups(name)
    VALUES (p_group_name)
    ON CONFLICT (name) DO NOTHING;

    SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;
    SELECT id INTO v_contact_id FROM contacts WHERE name = p_name;

    IF v_contact_id IS NULL THEN
        INSERT INTO contacts(name, email, birthday, group_id)
        VALUES (p_name, NULLIF(TRIM(p_email), ''), p_birthday, v_group_id)
        RETURNING id INTO v_contact_id;
    ELSE
        UPDATE contacts
        SET email = NULLIF(TRIM(p_email), ''),
            birthday = p_birthday,
            group_id = v_group_id
        WHERE id = v_contact_id;
    END IF;

    IF p_phone IS NOT NULL AND TRIM(p_phone) <> '' THEN
        SELECT contact_id INTO v_existing_contact_id
        FROM phones
        WHERE phone = p_phone;

        IF v_existing_contact_id IS NULL THEN
            INSERT INTO phones(contact_id, phone, type)
            VALUES (v_contact_id, p_phone, COALESCE(p_phone_type, 'mobile'));
        ELSIF v_existing_contact_id = v_contact_id THEN
            UPDATE phones
            SET type = COALESCE(p_phone_type, 'mobile')
            WHERE phone = p_phone;
        ELSE
            RAISE EXCEPTION 'Phone % already belongs to another contact', p_phone;
        END IF;
    END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INT;
BEGIN
    IF p_phone !~ '^\+?[0-9]{10,15}$' THEN
        RAISE EXCEPTION 'Incorrect phone: %', p_phone;
    END IF;

    IF p_type NOT IN ('home', 'work', 'mobile') THEN
        RAISE EXCEPTION 'Incorrect phone type: %', p_type;
    END IF;

    SELECT id INTO v_contact_id
    FROM contacts
    WHERE name = p_contact_name;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact not found: %', p_contact_name;
    END IF;

    INSERT INTO phones(contact_id, phone, type)
    VALUES (v_contact_id, p_phone, p_type);
END;
$$;


CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_group_id INT;
BEGIN
    INSERT INTO groups(name)
    VALUES (p_group_name)
    ON CONFLICT (name) DO NOTHING;

    SELECT id INTO v_group_id
    FROM groups
    WHERE name = p_group_name;

    UPDATE contacts
    SET group_id = v_group_id
    WHERE name = p_contact_name;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Contact not found: %', p_contact_name;
    END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE delete_contact(
    p_name VARCHAR DEFAULT NULL,
    p_phone VARCHAR DEFAULT NULL
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INT;
BEGIN
    IF p_name IS NULL AND p_phone IS NULL THEN
        RAISE EXCEPTION 'Give contact name or phone';
    END IF;

    IF p_name IS NOT NULL THEN
        DELETE FROM contacts
        WHERE name = p_name;
        RETURN;
    END IF;

    IF p_phone IS NOT NULL THEN
        SELECT contact_id INTO v_contact_id
        FROM phones
        WHERE phone = p_phone;

        IF v_contact_id IS NOT NULL THEN
            DELETE FROM contacts WHERE id = v_contact_id;
        END IF;
    END IF;
END;
$$;
