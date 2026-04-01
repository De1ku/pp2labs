CREATE OR REPLACE FUNCTION search_contacts(p_pattern text)
RETURNS TABLE(
    id int,
    username varchar,
    surname varchar,
    phone varchar
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.username, c.surname, c.phone
    FROM phonebook c
    WHERE c.username ILIKE '%' || p_pattern || '%'
       OR COALESCE(c.surname, '') ILIKE '%' || p_pattern || '%'
       OR c.phone ILIKE '%' || p_pattern || '%'
    ORDER BY c.id;
END;
$$;


CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit int, p_offset int)
RETURNS TABLE(
    id int,
    username varchar,
    surname varchar,
    phone varchar
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.username, c.surname, c.phone
    FROM phonebook c
    ORDER BY c.id
    LIMIT p_limit OFFSET p_offset;
END;
$$;