-- name: get-notifications-by-user-id
SELECT id,
       user_id,
       type,
       message,
       is_read,
       created_at,
       updated_at
FROM notifications
WHERE user_id = :user_id
ORDER BY created_at DESC;


-- name: get-notification-by-id^
SELECT id,
       user_id,
       type,
       message,
       is_read,
       created_at,
       updated_at
FROM notifications
WHERE id = :id AND user_id = :user_id
LIMIT 1;


-- name: create-new-notification<!
INSERT INTO notifications (user_id, type, message)
VALUES (:user_id, :type, :message)
RETURNING
    id, is_read, created_at, updated_at;


-- name: mark-notification-as-read<!
UPDATE notifications
SET is_read = true
WHERE id = :id AND user_id = :user_id
RETURNING
    updated_at;


-- name: delete-notification-by-id!
DELETE FROM notifications
WHERE id = :id AND user_id = :user_id;
