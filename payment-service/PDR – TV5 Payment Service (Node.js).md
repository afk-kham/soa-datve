# PDR – TV5 Payment Service (Node.js)

**Dự án:** Hệ thống đặt vé xem phim theo kiến trúc Microservices  
**Thành viên:** TV5  
**Công nghệ giữa kỳ:** Node.js 18+, module `http`, driver `mongodb`  
**Cuối kỳ:** Express + Mongoose + `jsonwebtoken`  
**Cổng:** `5005` · **CSDL:** `payment_db` · **Collection:** `transactions`

## 1. Mục đích và phạm vi

TV5 xây dựng Payment Service để tiếp nhận yêu cầu thanh toán từ Booking Service, mô phỏng kết quả thanh toán, lưu lịch sử giao dịch và cung cấp màn hình admin chỉ xem. Giữa kỳ chỉ làm bằng module `http` và driver MongoDB; không dùng Express/Mongoose.

**Ngoài phạm vi giữa kỳ:** gọi cổng thanh toán thật, tích hợp ví thật, JWT thật, gọi chéo Booking/Notification và chuyển sang framework. Các nội dung này là backlog cuối kỳ.

## 2. Đầu ra phải nộp (P1–P8)

| Mã | Đầu ra | Việc cần hoàn thành | Tiêu chí nghiệm thu |
|---|---|---|---|
| P1 | CSDL + seed | Tạo `payment_db.transactions`; viết `seed.js` chạy bằng `mongosh`; nạp 2 giao dịch A.5 | Đủ 2 dòng: `(1,180000,MOMO,PAID)` và `(2,85000,VNPAY,FAILED)`; `bookingId` là Number |
| P2 | ERD | Vẽ collection như một thực thể; ghi kiểu từng trường; nét đứt cho FK logic tới `bookings.id` | Có `_id:ObjectId`, `bookingId:Number`, `amount:Number`, `method:String`, `status:String`, `paidAt:Date` |
| P3 | Use Case | Actor Booking Service và Admin; xử lý, lưu, xem lịch sử | Sơ đồ và mô tả ngắn từng use case |
| P4 | DFD mức 0/1 | Mức 0: Booking/Admin ↔ Payment; mức 1: tiếp nhận, xử lý/ghi, truy vấn | Có kho D1 – transactions và luồng dữ liệu |
| P5 | DFD mức 2 | Phân rã 2.0 thành 2.1 kiểm tra, 2.2 giả lập, 2.3 ghi, 2.4 phản hồi | Luồng PAID/FAILED được thể hiện rõ |
| P6 | API | `POST /api/payment`, `GET /api/payment`, CORS/OPTIONS, JSON lỗi | Đúng mã HTTP, body, trạng thái và lưu cả FAILED |
| P7 | Admin | `admin_payment.html`: bảng bookingId, amount, method, status, paidAt | Gọi GET, hiển thị được dữ liệu và thông báo khi service lỗi |
| P8 | Báo cáo | Mô tả kiến trúc, dữ liệu, API, sơ đồ, ảnh Compass, ảnh curl, hạn chế | Có hướng dẫn chạy và checklist tự kiểm tra |

## 3. Mô hình dữ liệu

`transactions`: `_id:ObjectId` tự sinh; `bookingId:Number` FK logic → `Booking.bookings.id`; `amount:Number` VND; `method:String` thuộc `MOMO|VNPAY|CASH`; `status:String` thuộc `PAID|FAILED`; `paidAt:Date`.

### Seed mong muốn

```js
use payment_db;
db.transactions.deleteMany({});
db.transactions.insertMany([
  { bookingId: 1, amount: 180000, method: "MOMO",  status: "PAID",   paidAt: ISODate("2026-10-01T10:00:00Z") },
  { bookingId: 2, amount: 85000,  method: "VNPAY", status: "FAILED", paidAt: ISODate("2026-10-01T10:05:00Z") }
]);
```

## 4. Quy tắc API giữa kỳ

- `POST /api/payment`: đọc body qua sự kiện `data`/`end`, `JSON.parse` trong `try/catch`.
- `amount > 0` và `method` hợp lệ ⇒ `PAID`; ngược lại ⇒ `FAILED`, **vẫn lưu giao dịch**.
- Trả `201` cho yêu cầu tạo hợp lệ về cấu trúc; lỗi JSON/thiếu trường có thể trả `400` nhưng cần thống nhất với nhóm.
- `GET /api/payment`: `200` + mảng giao dịch, sắp xếp mới nhất trước nếu có thể.
- `OPTIONS`: trả `204` cùng CORS headers.
- Lắng nghe `0.0.0.0:5005`; Content-Type `application/json; charset=utf-8`.
- Giữa kỳ endpoint công khai để kiểm thử; cuối kỳ `POST`/`GET` áp dụng JWT theo hợp đồng chung, GET chỉ ADMIN.

## 5. Kế hoạch triển khai

1. Chuẩn bị Node.js 18+, MongoDB và Compass; tạo thư mục `payment-service/`.
2. Viết `config.example`, `.gitignore`, `package.json`, `payment_service.js`, `seed.js`, `admin_payment.html`.
3. Kết nối `mongodb://127.0.0.1:27017/payment_db`; không ghi mật khẩu thật vào repository.
4. Implement CORS, router, đọc body, validate, insert, list, error handler.
5. Seed và kiểm tra bằng Compass.
6. Chạy curl cho nhánh PAID, FAILED, JSON lỗi và GET.
7. Chụp ảnh API/Compass, hoàn thiện ERD–Use Case–DFD và báo cáo.
8. Bàn giao endpoint, cổng, cấu trúc JSON và dữ liệu seed cho TV4/TV6 khi ghép.

## 6. Kịch bản kiểm thử bắt buộc

| Mã | Input | Kỳ vọng |
|---|---|---|
| T01 | bookingId 3, amount 180000, MOMO | 201, PAID, lưu Number |
| T02 | bookingId 2, amount 85000, VNPAY | 201, PAID nếu amount/method hợp lệ |
| T03 | amount 0, MOMO | 201 hoặc quy ước thống nhất, FAILED và vẫn lưu |
| T04 | amount -1, CASH | FAILED và vẫn lưu |
| T05 | method BANK | FAILED và vẫn lưu |
| T06 | JSON sai cú pháp | 400, không làm sập server |
| T07 | GET /api/payment | 200, mảng giao dịch |
| T08 | OPTIONS | 204, đủ CORS headers |

## 7. Rủi ro và bàn giao

- `bookingId` bị lưu thành chuỗi: ép/kiểm tra Number trước insert.
- Quên lưu FAILED: kiểm thử riêng amount ≤ 0 và method sai.
- JSON parse làm sập server: luôn có `try/catch`.
- Compass không thấy dữ liệu: kiểm tra đúng DB/collection và URI.
- Lệch hợp đồng JSON: thống nhất với nhóm trước khi ghép.

## 8. Checklist trước khi nộp

- [ ] P1–P8 hoàn thành, file nguồn và ảnh minh chứng có tên đúng.
- [ ] `node payment_service.js` chạy ở `0.0.0.0:5005`.
- [ ] `mongosh < seed.js` chạy thành công.
- [ ] Có 2 giao dịch A.5 và có `paidAt` kiểu Date.
- [ ] Có ảnh Compass, ảnh curl POST/GET, ảnh admin.
- [ ] Báo cáo ghi rõ giữa kỳ dùng `http` + `mongodb`; cuối kỳ mới dùng Express + Mongoose.
