# Notification Service — TV6, bản giữa kỳ

Project độc lập trong `D:\workspace\SOA\project_final`. Notification nhận yêu cầu thông báo đặt vé, tự soạn nội dung, gửi **giả lập** bằng console và lưu MySQL riêng. Không gọi service khác, không đọc booking_db, không gửi email/SMS thật. API giữa kỳ công khai, không yêu cầu JWT hay X-Internal-Key.

## Môi trường và cấu trúc

Cần Go >= 1.22, MySQL 8.x, tài khoản được phép tạo database/bảng (hoặc nhờ quản trị tạo), Python 3 để phục vụ admin. Go đã được tải từ go.dev, đối chiếu SHA256 và đặt tại `.tools/go` (không đưa vào Git). Nếu đã cài Go, có thể dùng Go trong PATH.

| File/thư mục | Vai trò |
|---|---|
| main.go | DB chung, HTTP server, timeout và đóng tài nguyên Ctrl+C |
| config.go / config.example | Đọc/kiểm tra biến môi trường / mẫu cấu hình |
| model.go / response.go | DTO, envelope JSON |
| handler.go | Routing chính xác, validation, xử lý hai endpoint |
| notification.go | Soạn nội dung và console sender |
| store.go | SQL MySQL, placeholder, timeout, pool |
| middleware.go | CORS, request log, xử lý panic |
| *_test.go | Kiểm thử HTTP/config với fake store/sender |
| db/schema.sql / db/seed.sql | Bản schema và seed duy nhất |
| admin/admin_notification.html | Nhật ký chỉ xem, lọc cục bộ, tải lại |
| admin/index.html | Khung sáu tab, Notification nhúng bằng iframe |
| docs/ | API, thiết kế, kế hoạch cuối kỳ và kết quả kiểm tra |
| go.mod / go.sum | Dependency đã khóa checksum |

## Chạy trên Windows PowerShell

```powershell
Set-Location D:\workspace\SOA\project_final
$env:PATH = "$PWD\.tools\go\bin;" + $env:PATH
go mod download
```

Tạo schema, seed bằng MySQL CLI (nhập mật khẩu ở prompt; không đặt mật khẩu trong command). `SOURCE` đọc file UTF-8 trực tiếp, tránh pipe SQL qua PowerShell làm sai Unicode:

```powershell
mysql.exe --default-character-set=utf8mb4 -h 127.0.0.1 -P 3306 -u root -p --execute="SOURCE D:/workspace/SOA/project_final/db/schema.sql"
mysql.exe --default-character-set=utf8mb4 -h 127.0.0.1 -P 3306 -u root -p --execute="SOURCE D:/workspace/SOA/project_final/db/seed.sql"
```

Hoặc mở hai file SQL trong DBeaver và thực thi lần lượt trên kết nối MySQL. Kiểm tra `SHOW CREATE TABLE notification_db.notification_logs` nếu bảng đã tồn tại: schema chỉ CREATE IF NOT EXISTS, không sửa bảng cũ. Không có foreign key sang Booking. Seed dùng GET_LOCK để tuần tự hóa các lần chạy đồng thời; không dùng ID cố định, không xóa/ghi đè dữ liệu. Nếu đã có một dòng với cùng booking_id/username/channel/message, seed không thêm nữa. Nếu không lấy được lock trong 10 giây, không chèn; chạy lại và kiểm tra kết quả.

Ứng dụng **chỉ đọc biến môi trường**, không tự đọc `.env` hoặc `config.example`:

```powershell
$env:HTTP_ADDR = '0.0.0.0:5006'
$env:DB_HOST = '127.0.0.1'
$env:DB_PORT = '3306'
$env:DB_NAME = 'notification_db'
$env:DB_USER = 'your_notification_user' # thay bằng tài khoản của bạn
$secret = Read-Host 'Mật khẩu MySQL' -AsSecureString
$env:DB_PASSWORD = [System.Net.NetworkCredential]::new('', $secret).Password
go run .
# Ctrl+C dừng server và đóng DB; sau khi dừng:
Remove-Item Env:DB_PASSWORD
```

Service PingContext khi khởi động; DB không truy cập được thì thoát, không chạy chế độ giả. DB timeout 5 giây, pool tối đa 10 kết nối/5 idle, lifetime 3 phút. HTTP có read-header/read/write/idle timeout 5/10/15/60 giây. Không ghi mật khẩu/DSN/token vào log.

Terminal PowerShell thứ hai để kiểm tra CSDL thật:

```powershell
Invoke-RestMethod 'http://localhost:5006/api/notify/logs' | ConvertTo-Json -Depth 6
$body = @{ username = 'user1'; bookingId = 3; channel = 'EMAIL' } | ConvertTo-Json
$result = Invoke-RestMethod -Method Post -Uri 'http://localhost:5006/api/notify' -ContentType 'application/json; charset=utf-8' -Body ([System.Text.Encoding]::UTF8.GetBytes($body))
$result | ConvertTo-Json -Depth 6
$logs = Invoke-RestMethod 'http://localhost:5006/api/notify/logs'
if (-not ($logs.data | Where-Object id -eq $result.data.notificationId)) { throw 'Không thấy nhật ký vừa tạo' }
```

GET đầu tiên phải thấy dòng seed user1/đơn 1. POST trên thêm một dòng thật, không xóa dữ liệu. POST lặp lại sẽ tạo thêm dòng vì giữa kỳ chưa có idempotency.

## Chạy admin

```powershell
Set-Location D:\workspace\SOA\project_final
python -m http.server 8081 --bind 127.0.0.1 --directory admin
```

Mở `http://localhost:8081/` hoặc `http://localhost:8081/admin_notification.html`. Sau POST, bấm **Tải lại** để thấy dòng mới. Có thể mở file HTML trực tiếp nếu trình duyệt cho phép fetch; HTTP server là cách chạy chính.

Trang riêng có `API_BASE` ở đầu JavaScript. Trang chung có `SERVICE_API_URLS` cho 6 service; iframe Notification cùng origin đọc URL từ cấu hình này. Chỉ có Notification được tích hợp; 5 tab còn lại ghi **Chưa tích hợp**, đang chờ trang của thành viên khác. Iframe dùng lại nguyên trang riêng để không nhân bản logic; lỗi API Notification ở trong panel riêng. Không có dữ liệu giả, không có chức năng sửa/xóa/gửi trong admin. Dữ liệu API hiển thị bằng textContent.

Nếu chạy khác máy, đổi API_BASE và SERVICE_API_URLS.notification sang IP máy chạy API. `localhost` là máy của trình duyệt. Để admin truy cập từ LAN có thể bind HTTP static server `0.0.0.0`; cấu hình mạng theo môi trường của nhóm.

## API và thời gian

| Endpoint | Method | Kết quả |
|---|---|---|
| /api/notify | POST | 200, data có notificationId và deliveryStatus SIMULATED |
| /api/notify/logs | GET | 200, data là mảng log, rỗng là [] |
| Hai endpoint trên | OPTIONS | 204, không body |

Request POST: `{"username":"user1","bookingId":3,"channel":"EMAIL"}`. Envelope success: `{"status":"success","data":...}`; error: `{"status":"error","message":"..."}`. Mã lỗi: 400 JSON/validation, 413 quá 16 KiB, 404 đường dẫn lạ, 405 method sai (có Allow), 500 sender/store lỗi. Xem hợp đồng đầy đủ trong [docs/api.md](docs/api.md).

DATETIME lưu theo UTC, độ chính xác giây; kết nối MySQL dùng UTC, parseTime=true. API sentAt là RFC3339 UTC (`Z`); admin hiển thị múi giờ trình duyệt. Console và MySQL không có transaction chung: console có thể ghi SIMULATED trước khi INSERT lỗi; lúc đó API trả 500. Không coi dòng console là bằng chứng hoàn tất.

## Kiểm thử và build

```powershell
$env:PATH = "$PWD\.tools\go\bin;" + $env:PATH
$sources = (Get-ChildItem -Filter '*.go').FullName
gofmt -w $sources
go vet ./...
go test ./... -cover
go build ./...
New-Item -ItemType Directory -Force bin | Out-Null
go build -o bin/notification.exe .
.\bin\notification.exe # dùng cùng biến môi trường như go run
```

Kết quả thực tế và giới hạn xem [docs/verification.md](docs/verification.md). Fake store chỉ kiểm tra HTTP, không chứng minh MySQL đã tích hợp. Quy trình kiểm tra thật là tạo schema/seed, GET seed, POST, GET và tải lại admin như trên.

## Lỗi thường gặp

| Lỗi | Cách kiểm tra |
|---|---|
| DB chưa chạy / connection refused | Khởi động MySQL; kiểm tra host và cổng 3306 |
| Sai tài khoản | Thử đăng nhập CLI/DBeaver, kiểm tra quyền trên notification_db |
| Thiếu database/bảng hoặc schema cũ | Chạy schema.sql, kiểm tra SHOW CREATE TABLE; không tự xóa bảng |
| Cổng 5006/8081 bị chiếm | `Get-NetTCPConnection -LocalPort 5006,8081 -State Listen`; đổi HTTP_ADDR nếu cần và cập nhật API URL |
| Admin không kết nối | Kiểm tra service đang chạy, API_BASE, URL trang chung, mạng |
| Go không có trong PATH | Thêm `.tools/go/bin` bằng lệnh phía trên hoặc cài Go chính thức |
| Windows Application Control chặn test exe | Dùng môi trường Go được chính sách máy cho phép; không tắt bảo vệ máy |

Phần cuối kỳ chưa triển khai được ghi ở [docs/final-term-plan.md](docs/final-term-plan.md). Chưa ghép báo cáo nhóm vì chưa có 6 báo cáo; chưa tạo Word/draw.io.
