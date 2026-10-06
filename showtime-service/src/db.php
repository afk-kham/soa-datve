<?php
// Khởi tạo kết nối PDO MySQL
function db() {
    static $pdo = null;
    if ($pdo === null) {
        try {
            $pdo = new PDO("mysql:host=" . DB_HOST . ";dbname=" . DB_NAME . ";charset=utf8mb4", DB_USER, DB_PASS, [
                PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
                PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC
            ]);
        } catch (PDOException $e) {
            send_error("Lỗi kết nối CSDL: " . $e->getMessage(), 500);
        }
    }
    return $pdo;
}

// Format kết quả trả về cả movieId (cho showtime.html) và movie_id (cho API tiêu chuẩn)
function format_showtime_row($row) {
    if (!$row) return null;
    $mid = (int) $row['movie_id'];
    return [
        'id'       => (int) $row['id'],
        'movieId'  => $mid,      // Phục vụ giao diện showtime.html (r.movieId)
        'movie_id' => $mid,      // Phục vụ API Spec tiêu chuẩn
        'cinema'   => $row['cinema'],
        'room'     => $row['room'],
        'time'     => $row['time'],
        'price'    => (int) $row['price']
    ];
}

// Tìm danh sách suất chiếu (có lọc movieId nếu truyền vào)
function find_showtimes($movieId = null) {
    if ($movieId !== null) {
        $st = db()->prepare('SELECT * FROM showtimes WHERE movie_id = ? ORDER BY id ASC');
        $st->execute([$movieId]);
    } else {
        $st = db()->query('SELECT * FROM showtimes ORDER BY id ASC');
    }
    return array_map('format_showtime_row', $st->fetchAll());
}

// Tìm 1 suất chiếu theo ID
function find_showtime($id) {
    $st = db()->prepare('SELECT * FROM showtimes WHERE id = ?');
    $st->execute([$id]);
    $row = $st->fetch();
    return $row ? format_showtime_row($row) : null;
}