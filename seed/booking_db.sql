CREATE DATABASE IF NOT EXISTS booking_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE booking_db;

DROP TABLE IF EXISTS bookings;
CREATE TABLE bookings (
  id INT AUTO_INCREMENT PRIMARY KEY,
  movie_id INT NOT NULL,          -- FK logic -> Movie
  showtime_id INT NOT NULL,       -- FK logic -> Showtime
  username VARCHAR(50) NOT NULL,  -- FK logic -> User
  seats VARCHAR(100) NOT NULL,    -- ví dụ 'A1,A2'
  total_price INT NOT NULL,
  status VARCHAR(10) NOT NULL DEFAULT 'PENDING',   -- PENDING | PAID | CANCELLED
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO bookings (id, movie_id, showtime_id, username, seats, total_price, status, created_at) VALUES
(1, 1, 1, 'user1', 'A1,A2', 180000, 'PAID',      '2026-10-01 10:00:00'),
(2, 2, 3, 'user2', 'B5',     85000, 'CANCELLED', '2026-10-01 11:00:00'),
(3, 4, 5, 'user1', 'C3,C4', 180000, 'PENDING',   '2026-10-02 09:30:00');
