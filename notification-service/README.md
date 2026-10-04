# Notification Service – TV6 (Go)

| Mục | Nội dung |
|-----|----------|
| Branch | `tv6-notification` |
| Cổng | **5006** (lắng nghe `0.0.0.0`) |
| CSDL | MySQL `notification_db` (đề xuất, chờ thầy xác nhận) |
| Giữa kỳ (core) | `net/http` + `database/sql` + go-sql-driver/mysql |
| Cuối kỳ (framework) | `net/http` cấu trúc lại (handler/store, middleware X-Internal-Key, graceful shutdown) |
| Dữ liệu mẫu | `seed/notification_db.sql` |
| Trang admin | `admin/pages/admin_notification.html (chỉ xem)` |

## API (giữa kỳ)

- `POST /api/notify`
- `GET /api/notify/logs`

Quy ước: JSON `{"status":"success","data":…}` hoặc `{"status":"error","message":"…"}`; có CORS và xử lý `OPTIONS` (204); truy vấn có tham số.

## Cách chạy

- Giữa kỳ: `go run .`
- Cuối kỳ: `go run ./cmd/notification`

## Việc cần làm

- [ ] P1 CSDL + seed khớp `seed/`
- [ ] P2 ERD (`docs/tv6-notification/`)
- [ ] P3 Use Case
- [ ] P4 DFD mức 0, 1
- [ ] P5 DFD mức 2
- [ ] P6 API code thuần chạy được
- [ ] P7 Trang admin
- [ ] P8 Báo cáo chức năng

Chi tiết xem `docs/tai-lieu/Phieu_Giao_Viec_Chuan_Bi_Giua_Ky.docx` (Phần 6, phiếu riêng TV6).
