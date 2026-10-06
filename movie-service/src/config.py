import os

# Cấu hình CSDL MySQL cho Movie Service
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = int(os.environ.get("DB_PORT", 3306))
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")  # Mặc định của XAMPP/WAMP thường để trống
DB_NAME = os.environ.get("DB_NAME", "movie_db")
DB_CHARSET = "utf8mb4"

# Cấu hình máy chủ HTTP Movie Service (Theo hợp đồng SOA)
SERVER_HOST = os.environ.get("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.environ.get("SERVER_PORT", 5001))
