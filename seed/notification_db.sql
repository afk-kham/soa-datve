CREATE DATABASE IF NOT EXISTS notification_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE notification_db;

DROP TABLE IF EXISTS notification_logs;
CREATE TABLE notification_logs (
  id INT AUTO_INCREMENT PRIMARY KEY,
  booking_id INT,                 -- FK logic -> Booking
  username VARCHAR(50),
  channel VARCHAR(20),            -- EMAIL | SMS
  message VARCHAR(255),
  sent_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO notification_logs (id, booking_id, username, channel, message, sent_at) VALUES
(1, 1, 'user1', 'EMAIL', 'Đặt vé thành công cho đơn #1', '2026-10-01 10:02:00');
