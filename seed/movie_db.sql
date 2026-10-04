CREATE DATABASE IF NOT EXISTS movie_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE movie_db;

DROP TABLE IF EXISTS movies;
CREATE TABLE movies (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  genre VARCHAR(100),
  duration INT,
  poster VARCHAR(255)
);

INSERT INTO movies (id, title, genre, duration, poster) VALUES
(1, 'Avengers: Endgame', 'Hành động', 181, 'poster1.jpg'),
(2, 'Inception', 'Khoa học viễn tưởng', 148, 'poster2.jpg'),
(3, 'Parasite', 'Tâm lý', 132, 'poster3.jpg'),
(4, 'Mai', 'Tâm lý', 131, 'poster4.jpg'),
(5, 'Coco', 'Hoạt hình', 105, 'poster5.jpg');
