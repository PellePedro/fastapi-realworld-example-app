-- name: get-all-authors
SELECT a.id,
       a.user_id,
       u.username,
       a.specialty,
       a.location,
       a.website,
       a.created_at,
       a.updated_at
FROM authors a
JOIN users u ON a.user_id = u.id;


-- name: get-author-by-username^
SELECT a.id,
       a.user_id,
       u.username,
       a.specialty,
       a.location,
       a.website,
       a.created_at,
       a.updated_at
FROM authors a
JOIN users u ON a.user_id = u.id
WHERE u.username = :username
LIMIT 1;


-- name: create-new-author<!
INSERT INTO authors (user_id, specialty, location, website)
VALUES (:user_id, :specialty, :location, :website)
RETURNING
    id, created_at, updated_at;


-- name: update-author-by-user-id<!
UPDATE authors
SET specialty = :specialty,
    location  = :location,
    website   = :website
WHERE user_id = :user_id
RETURNING
    updated_at;


-- name: delete-author-by-user-id!
DELETE FROM authors
WHERE user_id = :user_id;
