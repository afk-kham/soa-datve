# BÁO CÁO TIẾN ĐỘ TV5 – PAYMENT SERVICE

## 1. Thông tin chung

- **Đề tài:** Hệ thống đặt vé xem phim theo kiến trúc Microservices
- **Thành viên:** TV5
- **Dịch vụ:** Payment Service
- **Cổng chạy:** `5005`
- **Cơ sở dữ liệu:** MongoDB `payment_db`
- **Collection:** `transactions`
- **Phạm vi báo cáo:** Kiểm tra quá trình/giữa kỳ

> Báo cáo này chỉ trình bày phần giữa kỳ: Node.js module `http` + driver `mongodb`. Chưa triển khai Express, Mongoose, JWT và gọi chéo Booking/Notification của giai đoạn cuối kỳ.

## 2. Mục tiêu và phạm vi chức năng

Payment Service tiếp nhận yêu cầu thanh toán giả lập từ Booking Service, xác định trạng thái thanh toán, lưu lịch sử giao dịch vào MongoDB và cung cấp trang admin chỉ xem.

| Nhóm chức năng | Nội dung | Trạng thái |
|---|---|---|
| Tiếp nhận thanh toán | `POST /api/payment` | Hoàn thành |
| Giả lập kết quả | `PAID` nếu `amount > 0` và method hợp lệ; ngược lại `FAILED` | Hoàn thành |
| Lưu giao dịch | Ghi cả giao dịch `PAID` và `FAILED` | Hoàn thành |
| Xem lịch sử | `GET /api/payment` | Hoàn thành |
| Trang admin | Bảng giao dịch, thông báo lỗi service | Hoàn thành |
| Bảo mật JWT | Xác thực và giới hạn ADMIN | Để cuối kỳ |
| Thanh toán thật | MoMo/VNPay thật | Ngoài phạm vi |

## 3. Phân tích sơ đồ Use Case mức ý niệm

### 3.1. Actor

- **Booking Service:** gửi yêu cầu thanh toán và nhận kết quả.
- **Admin:** xem lịch sử giao dịch trên trang quản trị.
- **Payment Service:** hệ thống xử lý trung gian và lưu dữ liệu.

### 3.2. Các Use Case

| Use Case | Actor | Mô tả |
|---|---|---|
| UC-01: Xử lý thanh toán | Booking Service | Gửi `bookingId`, `amount`, `method`; nhận trạng thái `PAID` hoặc `FAILED`. |
| UC-02: Kiểm tra yêu cầu | Payment Service | Kiểm tra kiểu dữ liệu và các trường bắt buộc. |
| UC-03: Giả lập kết quả | Payment Service | Xác định `PAID` khi amount dương và method thuộc `MOMO`, `VNPAY`, `CASH`; ngược lại là `FAILED`. |
| UC-04: Lưu giao dịch | Payment Service | Ghi giao dịch vào `payment_db.transactions`, bao gồm cả `FAILED`. |
| UC-05: Xem lịch sử giao dịch | Admin | Gọi GET và xem danh sách giao dịch mới nhất trước. |

![Use Case](https://private-us-east-1.manuscdn.com/sessionFile/PZsw7qy1OxpyF88PhY3Q7b/sandbox/Vt6WnIRSH6b7N5ArfcZL75-images_1791127520979_na1fn_L2hvbWUvdWJ1bnR1L3BheW1lbnRfc2VydmljZV9kZWxpdmVyeS9wYXltZW50LXNlcnZpY2UvZGlhZ3JhbXMvdXNlLWNhc2U.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvUFpzdzdxeTFPeHB5Rjg4UGhZM1E3Yi9zYW5kYm94L1Z0NlduSVJTSDZiN041QXJmY1pMNzUtaW1hZ2VzXzE3OTExMjc1MjA5NzlfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwzQmhlVzFsYm5SZmMyVnlkbWxqWlY5a1pXeHBkbVZ5ZVM5d1lYbHRaVzUwTFhObGNuWnBZMlV2WkdsaFozSmhiWE12ZFhObExXTmhjMlUucG5nIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNzkzNDkxMjAwfX19XX0_&Key-Pair-Id=K2QY5QTL8JSY6C&Signature=MEUCIBxB2rYn14zwNlnTF4W91synUo42uOkEoL5Z9HgP4R~nAiEAplYYoIYGnsGNo6I~Stfq6Vet1FedISxC8wfW7oxSX6I_)

Nguồn sơ đồ: [diagrams/use-case.mmd](diagrams/use-case.mmd).

## 4. DFD mức 1

### 4.1. Thành phần

- **Tác nhân ngoài:** Booking Service, Admin.
- **Tiến trình:** 1.0 Tiếp nhận yêu cầu, 2.0 Xử lý thanh toán, 3.0 Truy vấn lịch sử.
- **Kho dữ liệu:** D1 – `transactions`.

### 4.2. Luồng dữ liệu

1. Booking Service gửi thông tin thanh toán tới tiến trình 1.0.
2. Tiến trình 1.0 chuyển dữ liệu hợp lệ sang 2.0.
3. Tiến trình 2.0 tạo trạng thái `PAID` hoặc `FAILED`, ghi D1 và trả kết quả cho Booking.
4. Admin gửi yêu cầu xem lịch sử tới 3.0.
5. Tiến trình 3.0 đọc D1 và trả danh sách giao dịch cho Admin.

![DFD mức 1](https://private-us-east-1.manuscdn.com/sessionFile/PZsw7qy1OxpyF88PhY3Q7b/sandbox/Vt6WnIRSH6b7N5ArfcZL75-images_1791127520979_na1fn_L2hvbWUvdWJ1bnR1L3BheW1lbnRfc2VydmljZV9kZWxpdmVyeS9wYXltZW50LXNlcnZpY2UvZGlhZ3JhbXMvZGZkLWxldmVsLTE.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvUFpzdzdxeTFPeHB5Rjg4UGhZM1E3Yi9zYW5kYm94L1Z0NlduSVJTSDZiN041QXJmY1pMNzUtaW1hZ2VzXzE3OTExMjc1MjA5NzlfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwzQmhlVzFsYm5SZmMyVnlkbWxqWlY5a1pXeHBkbVZ5ZVM5d1lYbHRaVzUwTFhObGNuWnBZMlV2WkdsaFozSmhiWE12Wkdaa0xXeGxkbVZzTFRFLnBuZyIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTc5MzQ5MTIwMH19fV19&Key-Pair-Id=K2QY5QTL8JSY6C&Signature=MEUCIQCbro5kAHwyV2m2q6U2aDE0ISwGP1shJc3rLfvefzjaLgIgcJKXOoW~4TuYxbV9x0FkYjGwg5P4PYSkjcRkJfI-qds_)

Nguồn sơ đồ: [diagrams/dfd-level-1.mmd](diagrams/dfd-level-1.mmd).

## 5. DFD mức 2 – Phân rã tiến trình 2.0

Tiến trình 2.0 được phân rã thành:

- **2.1 Kiểm tra yêu cầu:** kiểm tra `bookingId`, `amount`, `method`.
- **2.2 Giả lập thanh toán:** xác định `PAID` hoặc `FAILED`.
- **2.3 Ghi giao dịch:** lưu giao dịch và `paidAt` vào D1.
- **2.4 Phản hồi kết quả:** trả HTTP `201` và thông tin giao dịch.

Nhánh xử lý:

- `amount > 0` và method hợp lệ → `PAID` → ghi D1 → phản hồi thành công.
- `amount <= 0` hoặc method không hợp lệ → `FAILED` → vẫn ghi D1 → phản hồi thất bại.
- JSON sai hoặc thiếu trường bắt buộc → HTTP `400`, không ghi giao dịch.

![DFD mức 2](https://private-us-east-1.manuscdn.com/sessionFile/PZsw7qy1OxpyF88PhY3Q7b/sandbox/Vt6WnIRSH6b7N5ArfcZL75-images_1791127520979_na1fn_L2hvbWUvdWJ1bnR1L3BheW1lbnRfc2VydmljZV9kZWxpdmVyeS9wYXltZW50LXNlcnZpY2UvZGlhZ3JhbXMvZGZkLWxldmVsLTI.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvUFpzdzdxeTFPeHB5Rjg4UGhZM1E3Yi9zYW5kYm94L1Z0NlduSVJTSDZiN041QXJmY1pMNzUtaW1hZ2VzXzE3OTExMjc1MjA5NzlfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwzQmhlVzFsYm5SZmMyVnlkbWxqWlY5a1pXeHBkbVZ5ZVM5d1lYbHRaVzUwTFhObGNuWnBZMlV2WkdsaFozSmhiWE12Wkdaa0xXeGxkbVZzTFRJLnBuZyIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTc5MzQ5MTIwMH19fV19&Key-Pair-Id=K2QY5QTL8JSY6C&Signature=MEYCIQC17IcvM2pTcjg7DCW4HWa5~Md6Jc1IcgBQhw4hGXK--gIhAOYsmGRW~i6VxlnoUmm6Mehj7uXYicuM9SA5aoQ6zFDj)

Nguồn sơ đồ: [diagrams/dfd-level-2.mmd](diagrams/dfd-level-2.mmd).

## 6. Chức năng Admin

File thực hiện: `admin_payment.html`.

Trang admin gọi `GET http://localhost:5005/api/payment` và hiển thị các trường:

- `bookingId`
- `amount`
- `method`
- `status`
- `paidAt`

Trang có nút **Tải lại** và thông báo khi Payment Service không phản hồi hoặc trả mã lỗi. Trong giai đoạn giữa kỳ, trang này là màn hình chỉ xem; phân quyền JWT/ADMIN để cuối kỳ.

## 7. Mô hình dữ liệu và ERD cơ bản

### 7.1. Collection `transactions`

| Trường | Kiểu dữ liệu | Mô tả |
|---|---|---|
| `_id` | `ObjectId` | Khóa chính MongoDB tự sinh |
| `bookingId` | `Number` | Khóa ngoại logic tới `bookings.id` |
| `amount` | `Number` | Số tiền VND |
| `method` | `String` | `MOMO`, `VNPAY` hoặc `CASH` |
| `status` | `String` | `PAID` hoặc `FAILED` |
| `paidAt` | `Date` | Thời điểm ghi giao dịch |

`bookingId` chỉ là khóa ngoại logic vì Payment Service sở hữu database riêng; không tạo foreign key vật lý sang `booking_db`.

![ERD](https://private-us-east-1.manuscdn.com/sessionFile/PZsw7qy1OxpyF88PhY3Q7b/sandbox/Vt6WnIRSH6b7N5ArfcZL75-images_1791127520979_na1fn_L2hvbWUvdWJ1bnR1L3BheW1lbnRfc2VydmljZV9kZWxpdmVyeS9wYXltZW50LXNlcnZpY2UvZGlhZ3JhbXMvZXJk.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvUFpzdzdxeTFPeHB5Rjg4UGhZM1E3Yi9zYW5kYm94L1Z0NlduSVJTSDZiN041QXJmY1pMNzUtaW1hZ2VzXzE3OTExMjc1MjA5NzlfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwzQmhlVzFsYm5SZmMyVnlkbWxqWlY5a1pXeHBkbVZ5ZVM5d1lYbHRaVzUwTFhObGNuWnBZMlV2WkdsaFozSmhiWE12WlhKay5wbmciLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE3OTM0OTEyMDB9fX1dfQ__&Key-Pair-Id=K2QY5QTL8JSY6C&Signature=MEUCIHCGFKBmLXhWH5e0~OAUVVI0wgbHTLWwYooJPFelbYM-AiEA13AKm9ma56GpHaUsMG5RfVUOWDNRd4XA~01UDUu35PY_)

Nguồn sơ đồ: [diagrams/erd.mmd](diagrams/erd.mmd).

## 8. API đã cài đặt

### POST `/api/payment`

Request:

```json
{
  "bookingId": 3,
  "amount": 180000,
  "method": "MOMO"
}
```

Response thành công giả lập:

```json
{
  "message": "Thanh toán thành công",
  "transaction": {
    "bookingId": 3,
    "amount": 180000,
    "method": "MOMO",
    "status": "PAID",
    "paidAt": "2026-10-04T15:00:00.000Z"
  }
}
```

- HTTP `201`: request đúng cấu trúc, dù kết quả nghiệp vụ là `PAID` hay `FAILED`.
- HTTP `400`: JSON sai hoặc thiếu/trái kiểu trường bắt buộc.

### GET `/api/payment`

Trả HTTP `200` và mảng giao dịch, sắp xếp mới nhất trước.

### OPTIONS `/api/payment`

Trả HTTP `204` với CORS headers để hỗ trợ trình duyệt.

## 9. Dữ liệu mẫu và kiểm thử

`seed.js` nạp hai dòng mẫu:

| bookingId | amount | method | status |
|---:|---:|---|---|
| 1 | 180000 | MOMO | PAID |
| 2 | 85000 | VNPAY | FAILED |

Các trường hợp đã kiểm tra:

| Mã | Trường hợp | Kết quả |
|---|---|---|
| T01 | amount dương, MOMO | PAID |
| T02 | amount dương, VNPAY | PAID |
| T03 | amount bằng 0 | FAILED và vẫn lưu |
| T04 | amount âm | FAILED và vẫn lưu |
| T05 | method BANK | FAILED và vẫn lưu |
| T06 | JSON sai cú pháp | HTTP 400, server không dừng |
| T07 | GET danh sách | HTTP 200, trả mảng |
| T08 | OPTIONS | HTTP 204, có CORS |

## 10. Hướng dẫn chạy

```bash
npm install
mongosh < seed.js
npm start
```

Mở trang admin:

```bash
python3 -m http.server 8081
```

Truy cập `http://localhost:8081/admin_payment.html`.

## 11. Kết luận và phần còn lại

Phần giữa kỳ của TV5 đã có API lõi, cơ sở dữ liệu mẫu, giao diện admin và các sơ đồ phân tích cần trình bày. Các nội dung chưa làm vì dự án chưa đến giai đoạn cuối gồm Express, Mongoose, JWT, phân quyền ADMIN, gọi chéo Booking/Notification và cổng thanh toán thật.
