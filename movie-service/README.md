# Movie Service – TV1 (Python)

| Mục | Nội dung |
|-----|----------|
| Branch | `tv1-movie` |
| Cổng | **5001** (lắng nghe `0.0.0.0`) |
| CSDL | MySQL `movie_db` |
| Giữa kỳ (core) | `http.server` (BaseHTTPRequestHandler) + `pymysql` |
| Cuối kỳ (framework) | Django (ORM + Django Admin) + PyJWT |
| Dữ liệu mẫu | `seed/movie_db.sql` |
| Trang admin | `admin/pages/admin_movie.html (CRUD)` |

## API (giữa kỳ)

- `GET /api/movies`
- `GET /api/movies/{id}`
- `POST /api/movies`
- `PUT /api/movies/{id}`
- `DELETE /api/movies/{id}`

Quy ước: JSON `{"status":"success","data":…}` hoặc `{"status":"error","message":"…"}`; có CORS và xử lý `OPTIONS` (204); truy vấn có tham số.

## Cách chạy

- Giữa kỳ: `python movie_service.py`
- Cuối kỳ: `python manage.py runserver 0.0.0.0:5001`

## Việc cần làm

- [ ] P1 CSDL + seed khớp `seed/`
- [ ] P2 ERD (`docs/tv1-movie/`)
- [ ] P3 Use Case
- [ ] P4 DFD mức 0, 1
- [ ] P5 DFD mức 2
- [ ] P6 API code thuần chạy được
- [ ] P7 Trang admin
- [ ] P8 Báo cáo chức năng

Chi tiết xem `docs/tai-lieu/Phieu_Giao_Viec_Chuan_Bi_Giua_Ky.docx` (Phần 6, phiếu riêng TV1).
