CREATE OR REPLACE PROCEDURE upsert_contact(
    p_username varchar,
    p_surname varchar,
    p_phone varchar
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF p_phone !~ '^\+?[0-9]{10,15}$' THEN
        RAISE EXCEPTION 'Incorrect phone: %', p_phone;
    END IF;

    IF EXISTS (SELECT 1 FROM phonebook WHERE username = p_username) THEN
        UPDATE phonebook
        SET surname = p_surname,
            phone = p_phone
        WHERE username = p_username;
    ELSE
        INSERT INTO phonebook(username, surname, phone)
        VALUES (p_username, p_surname, p_phone);
    END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE insert_many_contacts(
    IN p_usernames text[],
    IN p_surnames text[],
    IN p_phones text[],
    INOUT p_bad_data text DEFAULT ''
)
LANGUAGE plpgsql
AS $$
DECLARE
    i int;
BEGIN
    p_bad_data := '';

    IF array_length(p_usernames, 1) IS DISTINCT FROM array_length(p_surnames, 1)
       OR array_length(p_usernames, 1) IS DISTINCT FROM array_length(p_phones, 1) THEN
        RAISE EXCEPTION 'Arrays must have the same length';
    END IF;

    FOR i IN 1..COALESCE(array_length(p_usernames, 1), 0) LOOP
        IF p_phones[i] !~ '^\+?[0-9]{10,15}$' THEN
            p_bad_data := p_bad_data ||
                '(' || p_usernames[i] || ', ' || COALESCE(p_surnames[i], '') || ', ' || p_phones[i] || '); ';
        ELSE
            BEGIN
                IF EXISTS (SELECT 1 FROM phonebook WHERE username = p_usernames[i]) THEN
                    UPDATE phonebook
                    SET surname = p_surnames[i],
                        phone = p_phones[i]
                    WHERE username = p_usernames[i];
                ELSE
                    INSERT INTO phonebook(username, surname, phone)
                    VALUES (p_usernames[i], p_surnames[i], p_phones[i]);
                END IF;
            EXCEPTION
                WHEN unique_violation THEN
                    p_bad_data := p_bad_data ||
                        '(' || p_usernames[i] || ', ' || COALESCE(p_surnames[i], '') || ', ' || p_phones[i] || ' - duplicate phone); ';
            END;
        END IF;
    END LOOP;
END;
$$;


CREATE OR REPLACE PROCEDURE delete_contact(
    p_username varchar DEFAULT NULL,
    p_phone varchar DEFAULT NULL
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF p_username IS NULL AND p_phone IS NULL THEN
        RAISE EXCEPTION 'Give username or phone';
    END IF;

    DELETE FROM phonebook
    WHERE username = p_username
       OR phone = p_phone;
END;
$$;