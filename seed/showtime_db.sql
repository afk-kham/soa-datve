CREATE DATABASE IF NOT EXISTS showtime_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE showtime_db;

DROP TABLE IF EXISTS showtimes;
CREATE TABLE showtimes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  movie_id INT NOT NULL,            -- FK logic -> movie_db.movies.id (KHÔNG tạo FOREIGN KEY thật)
  cinema VARCHAR(150),
  room VARCHAR(50),
  `time` DATETIME,
  price INT
);

INSERT INTO showtimes (id, movie_id, cinema, room, `time`, price) VALUES
(1, 1, 'CGV Vincom Đồng Khởi', 'P1', '2026-10-10 18:00:00', 90000),
(2, 1, 'CGV Vincom Đồng Khởi', 'P2', '2026-10-10 21:00:00', 100000),
(3, 2, 'Lotte Cinema Cantavil', 'P1', '2026-10-11 19:30:00', 85000),
(4, 3, 'BHD Star Bitexco', 'P3', '2026-10-11 20:00:00', 80000),
(5, 4, 'CGV Vincom Đồng Khởi', 'P3', '2026-10-12 17:30:00', 90000),
(6, 5, 'Lotte Cinema Cantavil', 'P2', '2026-10-12 15:00:00', 75000);
