# HƯỚNG DẪN CÀI ĐẶT & CHẠY TV1 - MOVIE SERVICE (PYTHON)

## 1. Yêu cầu môi trường
- Python 3.10 trở lên
- MySQL Server (XAMPP, MySQL Server 8.0, WampServer hoặc Docker)

## 2. Chuẩn bị Cơ sở dữ liệu
1. Mở MySQL Client (phpMyAdmin, MySQL Workbench hoặc DBeaver).
2. Chạy lần lượt 2 file trong thư mục `01_db`:
   - Chạy `schema.sql` để tạo CSDL `movie_db` và bảng `movies`.
   - Chạy `seed.sql` để nạp 5 phim mẫu theo quy ước chung của nhóm.

## 3. Cài đặt thư viện Python
Trong thư mục `03_code`:
```bash
pip install -r requirements.txt
```

## 4. Cấu hình CSDL (nếu mật khẩu root khác rỗng)
Mở file `config.py` và sửa thông tin tài khoản MySQL nếu cần:
```python
DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "root"
DB_PASSWORD = ""      # Điền mật khẩu MySQL nếu có
DB_NAME = "movie_db"
```

## 5. Chạy Service
Chạy lệnh sau trong thư mục `03_code`:
```bash
python movie_service.py
```
Server sẽ chạy trên cổng `5001` và lắng nghe tại `0.0.0.0:5001`.

## 6. Lệnh kiểm thử API (Testing)

### Lấy danh sách phim (GET):
```bash
curl http://localhost:5001/api/movies
```

### Lấy chi tiết một phim (GET):
```bash
curl http://localhost:5001/api/movies/1
```

### Thêm một bộ phim mới (POST):
```bash
curl.exe -X POST http://localhost:5001/api/movies -H "Content-Type: application/json" -d "{\"title\":\"Doraemon\",\"genre\":\"Hoạt hình\",\"duration\":95,\"poster\":\"doraemon.jpg\"}"
```

### Sửa thông tin phim (PUT):
```bash
curl.exe -X PUT http://localhost:5001/api/movies/1 -H "Content-Type: application/json" -d "{\"title\":\"Avengers: Endgame (Bản mở rộng)\",\"genre\":\"Hành động\",\"duration\":185,\"poster\":\"poster1_ext.jpg\"}"
```

### Xóa phim (DELETE):
```bash
curl.exe -X DELETE http://localhost:5001/api/movies/6
```
*(Lưu ý trên Windows PowerShell: Hãy gõ `curl.exe` thay vì `curl` để tránh nhầm với Invoke-WebRequest).*
