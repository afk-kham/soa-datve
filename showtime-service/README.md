# Showtime Service – TV2 (PHP)

| Mục | Nội dung |
|-----|----------|
| Branch | `tv2-showtime` |
| Cổng | **5002** (lắng nghe `0.0.0.0`) |
| CSDL | MySQL `showtime_db` |
| Giữa kỳ (core) | PHP thuần + PDO (router.php) |
| Cuối kỳ (framework) | CodeIgniter 4 (PHP 8.1+) + firebase/php-jwt |
| Dữ liệu mẫu | `seed/showtime_db.sql` |
| Trang admin | `admin/pages/admin_showtime.html (CRUD + lọc movie_id)` |

## API (giữa kỳ)

- `GET /api/showtimes?movie_id=`
- `GET /api/showtimes/{id}`
- `POST /api/showtimes`
- `PUT /api/showtimes/{id}`
- `DELETE /api/showtimes/{id}`

Quy ước: JSON `{"status":"success","data":…}` hoặc `{"status":"error","message":"…"}`; có CORS và xử lý `OPTIONS` (204); truy vấn có tham số.

## Cách chạy

- Giữa kỳ: `php -S 0.0.0.0:5002 router.php`
- Cuối kỳ: `php spark serve --host 0.0.0.0 --port 5002`

## Việc cần làm

- [ ] P1 CSDL + seed khớp `seed/`
- [ ] P2 ERD (`docs/tv2-showtime/`)
- [ ] P3 Use Case
- [ ] P4 DFD mức 0, 1
- [ ] P5 DFD mức 2
- [ ] P6 API code thuần chạy được
- [ ] P7 Trang admin
- [ ] P8 Báo cáo chức năng

Chi tiết xem `docs/tai-lieu/Phieu_Giao_Viec_Chuan_Bi_Giua_Ky.docx` (Phần 6, phiếu riêng TV2).
