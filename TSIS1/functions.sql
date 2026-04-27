DROP FUNCTION IF EXISTS search_contacts(TEXT);
DROP FUNCTION IF EXISTS get_contacts_paginated(INT, INT);
DROP FUNCTION IF EXISTS get_contacts_paginated(INT, INT, TEXT, TEXT, TEXT);

CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(
    contact_id INT,
    name VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    phones TEXT,
    created_at TIMESTAMP
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id,
        c.name,
        c.email,
        c.birthday,
        g.name,
        COALESCE(STRING_AGG(p.type || ': ' || p.phone, ', ' ORDER BY p.id), ''),
        c.created_at
    FROM contacts c
    LEFT JOIN groups g ON g.id = c.group_id
    LEFT JOIN phones p ON p.contact_id = c.id
    WHERE p_query IS NULL
       OR TRIM(p_query) = ''
       OR c.name ILIKE '%' || p_query || '%'
       OR COALESCE(c.email, '') ILIKE '%' || p_query || '%'
       OR COALESCE(g.name, '') ILIKE '%' || p_query || '%'
       OR EXISTS (
            SELECT 1
            FROM phones p2
            WHERE p2.contact_id = c.id
              AND p2.phone ILIKE '%' || p_query || '%'
       )
    GROUP BY c.id, c.name, c.email, c.birthday, g.name, c.created_at
    ORDER BY c.name;
END;
$$;


CREATE OR REPLACE FUNCTION get_contacts_paginated(
    p_limit INT,
    p_offset INT,
    p_group_name TEXT DEFAULT NULL,
    p_email_query TEXT DEFAULT NULL,
    p_sort_by TEXT DEFAULT 'name'
)
RETURNS TABLE(
    contact_id INT,
    name VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    phones TEXT,
    created_at TIMESTAMP
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id,
        c.name,
        c.email,
        c.birthday,
        g.name,
        COALESCE(STRING_AGG(p.type || ': ' || p.phone, ', ' ORDER BY p.id), ''),
        c.created_at
    FROM contacts c
    LEFT JOIN groups g ON g.id = c.group_id
    LEFT JOIN phones p ON p.contact_id = c.id
    WHERE (p_group_name IS NULL OR TRIM(p_group_name) = '' OR g.name = p_group_name)
      AND (p_email_query IS NULL OR TRIM(p_email_query) = '' OR COALESCE(c.email, '') ILIKE '%' || p_email_query || '%')
    GROUP BY c.id, c.name, c.email, c.birthday, g.name, c.created_at
    ORDER BY
        CASE WHEN LOWER(p_sort_by) = 'name' THEN c.name END ASC NULLS LAST,
        CASE WHEN LOWER(p_sort_by) = 'birthday' THEN c.birthday END ASC NULLS LAST,
        CASE WHEN LOWER(p_sort_by) IN ('date', 'created_at') THEN c.created_at END DESC NULLS LAST,
        c.id ASC
    LIMIT p_limit OFFSET p_offset;
END;
$$;
