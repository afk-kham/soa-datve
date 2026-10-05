SET NAMES utf8mb4;
USE notification_db;
-- Serialize concurrent seed runs; no fixed ID and no overwrite of existing rows.
SELECT GET_LOCK('notification_db.seed', 10) INTO @seed_lock;
INSERT INTO notification_logs (booking_id, username, channel, message, sent_at)
SELECT 1, 'user1', 'EMAIL', 'Đặt vé thành công cho đơn #1', '2026-01-01 00:00:00'
WHERE @seed_lock = 1 AND NOT EXISTS (
 SELECT 1 FROM notification_logs WHERE booking_id = 1 AND username = 'user1'
 AND channel = 'EMAIL' AND message = 'Đặt vé thành công cho đơn #1'
);
SELECT RELEASE_LOCK('notification_db.seed');
