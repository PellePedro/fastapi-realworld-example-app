-- name: get-all-categories
SELECT id,
       name,
       slug,
       description,
       created_at,
       updated_at
FROM categories;


-- name: get-category-by-slug^
SELECT id,
       name,
       slug,
       description,
       created_at,
       updated_at
FROM categories
WHERE slug = :slug
LIMIT 1;


-- name: create-new-category<!
INSERT INTO categories (name, slug, description)
VALUES (:name, :slug, :description)
RETURNING
    id, created_at, updated_at;


-- name: update-category-by-slug<!
UPDATE categories
SET name        = :new_name,
    slug        = :new_slug,
    description = :new_description
WHERE slug = :slug
RETURNING
    updated_at;


-- name: delete-category-by-slug!
DELETE FROM categories
WHERE slug = :slug;
