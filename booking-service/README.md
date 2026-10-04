# Booking Service – TV4 (C#)

| Mục | Nội dung |
|-----|----------|
| Branch | `tv4-booking` |
| Cổng | **5004** (lắng nghe `0.0.0.0`) |
| CSDL | SQL Server (Windows) hoặc MySQL `booking_db` |
| Giữa kỳ (core) | `HttpListener` + ADO.NET + System.Text.Json |
| Cuối kỳ (framework) | ASP.NET Core 8 Minimal API + EF Core + JWT middleware + HttpClientFactory |
| Dữ liệu mẫu | `seed/booking_db.sql (MySQL) hoặc seed/booking_db.sqlserver.sql` |
| Trang admin | `admin/pages/admin_booking.html (chỉ xem, nhãn trạng thái)` |

## API (giữa kỳ)

- `POST /api/booking`
- `GET /api/booking`
- `GET /api/booking/{id}`

Quy ước: JSON `{"status":"success","data":…}` hoặc `{"status":"error","message":"…"}`; có CORS và xử lý `OPTIONS` (204); truy vấn có tham số.

## Cách chạy

- Giữa kỳ: `dotnet run`
- Cuối kỳ: `dotnet run`

## Việc cần làm

- [ ] P1 CSDL + seed khớp `seed/`
- [ ] P2 ERD (`docs/tv4-booking/`)
- [ ] P3 Use Case
- [ ] P4 DFD mức 0, 1
- [ ] P5 DFD mức 2
- [ ] P6 API code thuần chạy được
- [ ] P7 Trang admin
- [ ] P8 Báo cáo chức năng

Chi tiết xem `docs/tai-lieu/Phieu_Giao_Viec_Chuan_Bi_Giua_Ky.docx` (Phần 6, phiếu riêng TV4).
