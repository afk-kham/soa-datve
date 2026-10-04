# Dữ liệu mẫu dùng chung

Mọi thành viên nạp **đúng** dữ liệu này để id khớp giữa các service. Có thể thêm dòng mới, **không đổi** các dòng có sẵn.

| File | Service | CSDL |
|------|---------|------|
| `movie_db.sql` | Movie | MySQL |
| `showtime_db.sql` | Showtime | MySQL |
| `user_db.sql` | User/Auth | MySQL |
| `booking_db.sql` / `booking_db.sqlserver.sql` | Booking | MySQL / SQL Server |
| `payment_db.js` | Payment | MongoDB (`mongosh payment_db.js`) |
| `notification_db.sql` | Notification | MySQL |

Tài khoản mẫu: `admin / Admin@123` (ADMIN), `user1 / User@123`, `user2 / User@123`.
Hash BCrypt dùng tiền tố `$2a$` (tương thích jBCrypt, Spring, .NET).

Nạp MySQL: `mysql -u root -p < seed/movie_db.sql`
