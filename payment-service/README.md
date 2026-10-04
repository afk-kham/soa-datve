# Payment Service – TV5 (Node.js)

| Mục | Nội dung |
|-----|----------|
| Branch | `tv5-payment` |
| Cổng | **5005** (lắng nghe `0.0.0.0`) |
| CSDL | MongoDB `payment_db` |
| Giữa kỳ (core) | module `http` + driver `mongodb` |
| Cuối kỳ (framework) | Express + Mongoose + jsonwebtoken |
| Dữ liệu mẫu | `seed/payment_db.js (mongosh)` |
| Trang admin | `admin/pages/admin_payment.html (chỉ xem)` |

## API (giữa kỳ)

- `POST /api/payment`
- `GET /api/payment`

Quy ước: JSON `{"status":"success","data":…}` hoặc `{"status":"error","message":"…"}`; có CORS và xử lý `OPTIONS` (204); truy vấn có tham số.

## Cách chạy

- Giữa kỳ: `node payment_service.js`
- Cuối kỳ: `node app.js`

## Việc cần làm

- [ ] P1 CSDL + seed khớp `seed/`
- [ ] P2 ERD (`docs/tv5-payment/`)
- [ ] P3 Use Case
- [ ] P4 DFD mức 0, 1
- [ ] P5 DFD mức 2
- [ ] P6 API code thuần chạy được
- [ ] P7 Trang admin
- [ ] P8 Báo cáo chức năng

Chi tiết xem `docs/tai-lieu/Phieu_Giao_Viec_Chuan_Bi_Giua_Ky.docx` (Phần 6, phiếu riêng TV5).
