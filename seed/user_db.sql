CREATE DATABASE IF NOT EXISTS user_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE user_db;

DROP TABLE IF EXISTS users;
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) NOT NULL UNIQUE,
  password_hash VARCHAR(100) NOT NULL,
  email VARCHAR(100),
  role VARCHAR(10) NOT NULL DEFAULT 'USER'   -- USER | ADMIN
);

-- Admin@123 và User@123 (BCrypt cost 10, tiền tố $2a$)
INSERT INTO users (id, username, password_hash, email, role) VALUES
(1, 'admin', '$2a$10$E8cofqiolfZk1ihu2plZM.UJfIuTvkB54LjgTxFBmeJwpY59Z/yju', 'admin@cinema.local', 'ADMIN'),
(2, 'user1', '$2a$10$ItvF/UzunDkYLpvNquq4iOP9vu4Z/gL0eoX3.FBvC1UaNSa2ugQ6O', 'user1@cinema.local', 'USER'),
(3, 'user2', '$2a$10$ItvF/UzunDkYLpvNquq4iOP9vu4Z/gL0eoX3.FBvC1UaNSa2ugQ6O', 'user2@cinema.local', 'USER');
