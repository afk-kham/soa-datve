# TV5 – Payment Service (Node.js)

Bản giữa kỳ dùng **Node.js 18+, module `http` và driver `mongodb`**, không dùng Express/Mongoose. Service lắng nghe `0.0.0.0:5005`, sử dụng `payment_db.transactions`.

## Cấu trúc
- `payment_service.js`: HTTP API, CORS/OPTIONS, parse JSON, validate, PAID/FAILED, MongoDB.
- `seed.js`: `mongosh` seed 2 giao dịch A.5.
- `admin_payment.html`: admin chỉ xem, gọi GET.
- `test_payment_service.js`: test logic không cần MongoDB.

## Chạy
```bash
npm install
cp .env.example .env
mongosh < seed.js
npm start
```
Mặc định MongoDB là `mongodb://127.0.0.1:27017/payment_db`.

Mở admin bằng static server:
```bash
python3 -m http.server 8081
# http://localhost:8081/admin_payment.html
```

## API
`POST /api/payment` body: `{"bookingId":3,"amount":180000,"method":"MOMO"}`.
`bookingId` phải là số nguyên dương; `amount` phải là số; `method` là chuỗi. `amount > 0` và method thuộc `MOMO|VNPAY|CASH` → `PAID`; ngược lại vẫn lưu `FAILED`. Body hợp lệ về cấu trúc trả `201`; JSON sai/thiếu trường trả `400`.

`GET /api/payment` trả `200` và mảng giao dịch mới nhất trước. `OPTIONS` trả `204` cùng CORS headers.

## Kiểm thử nhanh
```bash
npm test
curl -i -X POST http://localhost:5005/api/payment -H 'Content-Type: application/json' -d '{"bookingId":3,"amount":180000,"method":"MOMO"}'
curl -i -X POST http://localhost:5005/api/payment -H 'Content-Type: application/json' -d '{"bookingId":4,"amount":0,"method":"MOMO"}'
curl -i -X POST http://localhost:5005/api/payment -H 'Content-Type: application/json' -d '{"bookingId":5,"amount":85000,"method":"BANK"}'
curl -i -X POST http://localhost:5005/api/payment -H 'Content-Type: application/json' -d '{bad json'
curl -i http://localhost:5005/api/payment
curl -i -X OPTIONS http://localhost:5005/api/payment
```

## Checklist bàn giao
- [x] P1: seed bookingId 1/2, amount 180000/85000, MOMO/VNPAY, PAID/FAILED; `bookingId` là Number.
- [x] P6: POST, GET, OPTIONS, CORS, JSON lỗi; FAILED vẫn lưu.
- [x] P7: admin page có bảng và thông báo lỗi service.
- [x] Báo cáo quá trình: `BAO_CAO_TV5.md` và `BAO_CAO_TV5.pdf` gồm Use Case, DFD mức 1–2, ERD, admin và API.
- [x] Sơ đồ: thư mục `diagrams/` gồm Mermaid source và PNG.
- [x] Không chứa mật khẩu/secret thật.
- [ ] Bổ sung ảnh Compass/curl/admin thực tế nếu nhóm yêu cầu minh chứng chụp màn hình.
- [ ] Cuối kỳ: chuyển Express + Mongoose và thêm JWT/ADMIN.
