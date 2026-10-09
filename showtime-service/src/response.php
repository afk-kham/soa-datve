<?php
// Thiết lập Header CORS
function send_cors_headers() {
    header("Access-Control-Allow-Origin: *");
    header("Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS");
    header("Access-Control-Allow-Headers: Content-Type, Authorization, X-Requested-With");
}

// Trả về JSON Thành công
function send_success($data = null, $code = 200) {
    send_cors_headers();
    header("Content-Type: application/json; charset=UTF-8");
    http_response_code($code);
    echo json_encode(["status" => "success", "data" => $data], JSON_UNESCAPED_UNICODE);
    exit;
}

// Trả về JSON Báo lỗi
function send_error($message, $code = 400) {
    send_cors_headers();
    header("Content-Type: application/json; charset=UTF-8");
    http_response_code($code);
    echo json_encode(["status" => "error", "message" => $message], JSON_UNESCAPED_UNICODE);
    exit;
}