-- name: get-bookmarks-by-user-id
SELECT b.user_id,
       b.article_id,
       b.note,
       b.created_at,
       a.slug AS article_slug,
       a.title AS article_title
FROM bookmarks b
JOIN articles a ON b.article_id = a.id
WHERE b.user_id = :user_id;


-- name: get-bookmark^
SELECT b.user_id,
       b.article_id,
       b.note,
       b.created_at,
       a.slug AS article_slug,
       a.title AS article_title
FROM bookmarks b
JOIN articles a ON b.article_id = a.id
WHERE b.user_id = :user_id AND a.slug = :slug
LIMIT 1;


-- name: create-new-bookmark<!
INSERT INTO bookmarks (user_id, article_id, note)
VALUES (:user_id, :article_id, :note)
RETURNING
    created_at;


-- name: delete-bookmark!
DELETE FROM bookmarks
WHERE user_id = :user_id AND article_id = :article_id;
