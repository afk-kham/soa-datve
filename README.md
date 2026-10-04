# Hệ thống đặt vé xem phim – Kiến trúc hướng dịch vụ (SOA)

Bài tập lớn môn **Kiến trúc hướng dịch vụ**. Nhóm 6 thành viên, 6 service, 6 ngôn ngữ.
Giữa kỳ: viết API bằng **code thuần (core)**. Cuối kỳ: chuyển sang **framework**, thêm JWT, ghép thành hệ thống hoàn chỉnh.

## Các service

| TV | Service | Ngôn ngữ | Cổng | CSDL | Thư mục | Branch |
|----|---------|----------|------|------|---------|--------|
| 1 | Movie | Python (Core → Django) | 5001 | MySQL `movie_db` | `movie-service/` | `tv1-movie` |
| 2 | Showtime | PHP (Core → CodeIgniter 4) | 5002 | MySQL `showtime_db` | `showtime-service/` | `tv2-showtime` |
| 3 | User/Auth | Java (Core → Spring Boot 3.x) | 5003 | MySQL `user_db` | `user-service/` | `tv3-user` |
| 4 | Booking | C# (Core → ASP.NET Core 8) | 5004 | SQL Server/MySQL `booking_db` | `booking-service/` | `tv4-booking` |
| 5 | Payment | Node.js (Core → Express) | 5005 | MongoDB `payment_db` | `payment-service/` | `tv5-payment` |
| 6 | Notification | Go (`net/http`) | 5006 | MySQL `notification_db` | `notification-service/` | `tv6-notification` |

Giao diện: Client App cổng **8080** (`client/`), Admin Dashboard cổng **8081** (`admin/`).

## Cấu trúc kho

```
soa-datve/
├── docs/                  # sơ đồ & báo cáo (mỗi người 1 thư mục con) + tài liệu kế hoạch
├── movie-service/         # TV1 – Python
├── showtime-service/      # TV2 – PHP
├── user-service/          # TV3 – Java
├── booking-service/       # TV4 – C#
├── payment-service/       # TV5 – Node.js
├── notification-service/  # TV6 – Go
├── admin/                 # ghép từ admin/pages/admin_<service>.html
├── client/                # giao diện người dùng (cuối kỳ)
└── seed/                  # dữ liệu mẫu CHUNG (không đổi id)
```

## Quy trình Git (đọc kỹ)

Branch:

- `main`: bản ổn định, chỉ cập nhật ở các mốc (giữa kỳ, cuối kỳ). Không ai push trực tiếp.
- `develop`: nơi ghép phần của mọi người.
- `tv1-movie` … `tv6-notification`: **mỗi người làm trên branch của mình**.

Làm việc hằng ngày:

```bash
git clone <URL_KHO>
cd soa-datve
git checkout tv1-movie            # đổi thành branch của bạn
# ... làm việc trong thư mục của bạn ...
git add .
git commit -m "feat(movie): thêm API GET /api/movies"
git push origin tv1-movie
```

Khi xong một phần: mở **Pull Request** từ branch của bạn vào `develop`. Nhóm trưởng duyệt và merge.
Muốn lấy phần mới của người khác: `git checkout tv1-movie && git merge origin/develop`.

Quy ước:

1. **Chỉ sửa thư mục của mình** (service, `docs/<tv>/`, file admin của mình). Muốn sửa chỗ khác phải báo trước.
2. Dữ liệu mẫu trong `seed/` là chung: **không đổi id và giá trị** các dòng có sẵn.
3. Không commit mật khẩu, khóa thật, file `.env`. Dùng `.env.example` / `config.example`.
4. Tên commit: `feat(...)`, `fix(...)`, `docs(...)`, `chore(...)`. Ví dụ `docs(movie): thêm ERD`.
5. File sơ đồ: `UC_<service>.png`, `ERD_<service>.png`, `DFD0_…`, `DFD1_…`, `DFD2_…`, kèm file `.drawio`.

## Tài liệu

Xem thư mục `docs/tai-lieu/`: Kế hoạch triển khai v2.1 và Phiếu giao việc chuẩn bị giữa kỳ.
Hạn nộp phần chuẩn bị giữa kỳ: **20:00 Chủ nhật 04/10/2026**.

## Chạy nhanh

Mỗi service có README riêng trong thư mục của nó. Client/Admin: `python -m http.server 8080` hoặc `8081` trong thư mục tương ứng.
