<?php
// Đọc nội dung JSON body gửi từ Client/Postman/Admin UI
function read_json_body() {
    $input = file_get_contents('php://input');
    $data = json_decode($input, true);
    if ($input !== '' && $data === null) {
        send_error('Dữ liệu JSON không hợp lệ', 400);
    }
    return $data ?? [];
}

// Kiểm tra giá trị có phải dạng số nguyên không
function is_int_like($val) {
    return is_numeric($val) && (int)$val == $val;
}

// Validation dữ liệu cho thao tác POST và PUT
function validate_showtime(array $body, bool $isUpdate = false) {
    $mid = $body['movieId'] ?? $body['movie_id'] ?? null;
    $cinema = isset($body['cinema']) ? trim($body['cinema']) : null;
    $room = isset($body['room']) ? trim($body['room']) : null;
    $time = isset($body['time']) ? trim($body['time']) : null;
    $price = isset($body['price']) ? (int)$body['price'] : null;

    $res = [];

    if (!$isUpdate) {
        if ($mid === null || !is_int_like($mid) || (int)$mid <= 0) {
            send_error('movieId bắt buộc và phải là số nguyên dương', 400);
        }
        if (empty($cinema)) send_error('cinema không được để trống', 400);
        if (empty($room)) send_error('room không được để trống', 400);
        if (empty($time)) send_error('time không được để trống', 400);
        if ($price === null || $price < 0) send_error('price phải lớn hơn hoặc bằng 0', 400);

        $res = [
            'movie_id' => (int)$mid,
            'cinema'   => $cinema,
            'room'     => $room,
            'time'     => $time,
            'price'    => $price
        ];
    } else {
        if ($mid !== null) {
            if (!is_int_like($mid) || (int)$mid <= 0) send_error('movieId phải là số nguyên dương', 400);
            $res['movie_id'] = (int)$mid;
        }
        if ($cinema !== null) {
            if (empty($cinema)) send_error('cinema không được để trống', 400);
            $res['cinema'] = $cinema;
        }
        if ($room !== null) {
            if (empty($room)) send_error('room không được để trống', 400);
            $res['room'] = $room;
        }
        if ($time !== null) {
            if (empty($time)) send_error('time không được để trống', 400);
            $res['time'] = $time;
        }
        if ($price !== null) {
            if ($price < 0) send_error('price phải lớn hơn hoặc bằng 0', 400);
            $res['price'] = $price;
        }
        if (empty($res)) send_error('Không có dữ liệu nào được gửi để cập nhật', 400);
    }

    return $res;
}

// Kiểm tra phim có tồn tại bên Movie Service (cổng 5001) không
function assert_movie_exists($movieId) {
    $ctx = stream_context_create(['http' => ['timeout' => 1]]);
    $json = @file_get_contents(MOVIE_SERVICE_URL . '/' . $movieId, false, $ctx);
    if ($json !== false) {
        $res = json_decode($json, true);
        if (isset($res['status']) && $res['status'] === 'error') {
            send_error("Phim với ID = $movieId không tồn tại bên Movie Service", 400);
        }
    }
}