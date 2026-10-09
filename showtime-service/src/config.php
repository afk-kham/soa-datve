<?php
// Cấu hình kết nối CSDL showtime_db
define('DB_HOST', 'localhost');
define('DB_NAME', 'showtime_db');
define('DB_USER', 'root');
define('DB_PASS', '');

// URL kiểm tra tồn tại phim bên Movie Service (cổng 5001)
define('MOVIE_SERVICE_URL', 'http://localhost:5001/api/movies');
