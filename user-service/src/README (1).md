# User/Auth Service (TV3 – Java thuần, giữa kỳ)

`com.sun.net.httpserver.HttpServer` + JDBC (MySQL Connector/J) + jBCrypt + Gson. **Không dùng framework web.**
Cổng **5003**, lắng nghe `0.0.0.0`, CSDL MySQL `user_db`.

| Method & URL | Mô tả | Kết quả |
|---|---|---|
| `POST /api/login` | Body `{username,password}`, kiểm tra BCrypt | 200 `{id,username,role,token}` · 400 · 401 |
| `GET /api/users` | Danh sách người dùng (không có `password_hash`) | 200 mảng user |
| `OPTIONS *` | Preflight CORS | 204 |

## 1. Yêu cầu
Java 17+ · MySQL 8 (hoặc MariaDB 10.x) · (khuyên dùng) Maven 3.8+.

## 2. Tạo CSDL (chạy 1 lần)
```
mysql -u root -p < ../01_db/schema.sql
mysql -u root -p < ../01_db/seed.sql
```

## 3. Cấu hình kết nối
Mặc định nằm ở `src/main/java/userservice/Config.java` (user `root`, mật khẩu rỗng).
Ghi đè bằng biến môi trường, **không sửa/commit mật khẩu thật**:

PowerShell: `$env:DB_USER="root"; $env:DB_PASS="matkhau"`
bash: `export DB_USER=root DB_PASS=matkhau`
(Ngoài ra: `DB_URL`, `PORT`.)

## 4a. Chạy bằng Maven (dễ nhất)
```
mvn compile exec:java
```

## 4b. Chạy không cần Maven (IDE hoặc dòng lệnh)
Tải 3 file .jar vào thư mục `lib/`: `mysql-connector-j-8.x.jar`, `jbcrypt-0.4.jar`, `gson-2.10.1.jar`.

Windows (PowerShell):
```
mkdir out
javac -encoding UTF-8 -d out -cp "lib/*" src/main/java/userservice/*.java
java -cp "out;lib/*" userservice.Main
```
Linux/macOS: dùng `out:lib/*` thay cho `out;lib/*`.

Trong IDE (IntelliJ/Eclipse/NetBeans): thêm 3 jar vào classpath rồi chạy lớp `userservice.Main`.

Khi thành công sẽ in: `User Service dang chay tai http://0.0.0.0:5003`

## 5. Kiểm thử nhanh (dùng `curl.exe` trên PowerShell, hoặc Postman)
```
curl.exe -X POST http://localhost:5003/api/login -H "Content-Type: application/json" -d "{\"username\":\"user1\",\"password\":\"User@123\"}"
curl.exe http://localhost:5003/api/users
```
Tài khoản mẫu: `admin / Admin@123`, `user1 / User@123`, `user2 / User@123`.

## 6. Ghi chú thiết kế
* Truy vấn dùng `PreparedStatement` (tham số hoá), chống SQL injection.
* Sai username và sai mật khẩu cùng trả 401 với cùng một thông báo (không lộ tài khoản có tồn tại hay không).
* Không ghi mật khẩu thô hay hash ra log; `GET /api/users` không chọn cột `password_hash`.
* Token giữa kỳ là chuỗi tạm `demo-token-<username>`; cuối kỳ thay bằng JWT (Spring Boot + jjwt, khoá `Keys.hmacShaKeyFor(secret.getBytes(UTF_8))`).
