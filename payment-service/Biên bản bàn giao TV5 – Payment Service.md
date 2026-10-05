# Biên bản bàn giao TV5 – Payment Service

**Ngày:** 04/10/2026  
**Thành viên:** TV5  
**Phạm vi:** Bản giữa kỳ – Node.js core `http` + driver `mongodb`

## Đã hoàn thành

1. `payment_service.js`: service chạy `0.0.0.0:5005`, CORS/OPTIONS, `POST /api/payment`, `GET /api/payment`, `/health`, JSON lỗi an toàn, validate dữ liệu, giả lập `PAID/FAILED`, lưu MongoDB.
2. `seed.js`: tạo dữ liệu mẫu trong `payment_db.transactions`:
   - `bookingId=1`, `amount=180000`, `MOMO`, `PAID`.
   - `bookingId=2`, `amount=85000`, `VNPAY`, `FAILED`.
3. `admin_payment.html`: bảng admin chỉ xem, có thông báo lỗi khi service không khả dụng.
4. `package.json`, `package-lock.json`, `.env.example`, `.gitignore`, `README.md`.
5. `test_payment_service.js`: test logic PAID, FAILED, method sai, validate shape.
6. `BAO_CAO_TV5.md` và `BAO_CAO_TV5.pdf`: báo cáo kiểm tra quá trình gồm Use Case, DFD mức 1, DFD mức 2, chức năng admin, ERD và API.
7. `diagrams/`: mã nguồn Mermaid và ảnh PNG của 4 sơ đồ.

## Kết quả kiểm tra

- `npm test`: **4/4 passed**.
- `node --check payment_service.js`: đạt.
- `node --check seed.js`: đạt.
- HTTP contract test bằng collection giả lập: **đạt** cho 201 PAID, 201 FAILED, 400 JSON sai, 204 OPTIONS/CORS, 200 GET.

## Cách chạy để demo

```bash
npm install
mongosh < seed.js
npm start
```

Sau đó kiểm thử theo `README.md`; mở admin bằng `python3 -m http.server 8081` và truy cập `admin_payment.html`.

## Hồ sơ cần nộp lần kiểm tra quá trình

- Bổ sung ảnh Compass, ảnh curl POST/GET/OPTIONS và ảnh trang admin vào báo cáo chung nếu giảng viên yêu cầu minh chứng trực quan.
- Nộp `BAO_CAO_TV5.pdf` cùng thư mục source hoặc ZIP bàn giao.
- Khi làm cuối kỳ, chuyển sang Express + Mongoose và thêm `jsonwebtoken`, xác thực JWT; `GET` chỉ cho role `ADMIN` theo hợp đồng nhóm.
- Cần chạy `mongosh < seed.js` trên máy có MongoDB để xác nhận tích hợp thật; sandbox kiểm thử hiện dùng mock collection vì không có MongoDB daemon.
