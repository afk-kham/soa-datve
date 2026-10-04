# User/Auth Service – TV3 (Java)

| Mục | Nội dung |
|-----|----------|
| Branch | `tv3-user` |
| Cổng | **5003** (lắng nghe `0.0.0.0`) |
| CSDL | MySQL `user_db` |
| Giữa kỳ (core) | `com.sun.net.httpserver.HttpServer` + JDBC + jBCrypt |
| Cuối kỳ (framework) | Spring Boot 3.x + Spring Data JPA + jjwt 0.12.x |
| Dữ liệu mẫu | `seed/user_db.sql` |
| Trang admin | `admin/pages/admin_user.html (chỉ xem)` |

## API (giữa kỳ)

- `POST /api/login`
- `GET /api/users`

Quy ước: JSON `{"status":"success","data":…}` hoặc `{"status":"error","message":"…"}`; có CORS và xử lý `OPTIONS` (204); truy vấn có tham số.

## Cách chạy

- Giữa kỳ: `Chạy lớp Main (IDE hoặc java)`
- Cuối kỳ: `mvn spring-boot:run`

## Việc cần làm

- [ ] P1 CSDL + seed khớp `seed/`
- [ ] P2 ERD (`docs/tv3-user/`)
- [ ] P3 Use Case
- [ ] P4 DFD mức 0, 1
- [ ] P5 DFD mức 2
- [ ] P6 API code thuần chạy được
- [ ] P7 Trang admin
- [ ] P8 Báo cáo chức năng

Chi tiết xem `docs/tai-lieu/Phieu_Giao_Viec_Chuan_Bi_Giua_Ky.docx` (Phần 6, phiếu riêng TV3).
