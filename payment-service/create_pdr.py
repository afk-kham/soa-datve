from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_BREAK
from pathlib import Path

OUT = Path('/home/ubuntu/pdr_tv5')
DOCX = OUT / 'PDR_TV5_Payment_Service_Nodejs.docx'
MD = OUT / 'PDR_TV5_Payment_Service_Nodejs.md'

NAVY = '1F4E79'
BLUE = 'D9EAF7'
LIGHT = 'F3F6F9'
DARK = '1F2937'
GREEN = 'E2F0D9'
ORANGE = 'FCE4D6'


def shade(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = tcPr.find(qn('w:shd'))
    if shd is None:
        shd = OxmlElement('w:shd'); tcPr.append(shd)
    shd.set(qn('w:fill'), fill)


def set_cell_text(cell, text, bold=False, color=DARK, size=9.5):
    cell.text = ''
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run(str(text))
    r.bold = bold; r.font.size = Pt(size); r.font.color.rgb = RGBColor.from_string(color)
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER


def table(doc, headers, rows, widths=None, header_fill=NAVY):
    t = doc.add_table(rows=1, cols=len(headers))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.style = 'Table Grid'
    for i, h in enumerate(headers):
        set_cell_text(t.rows[0].cells[i], h, True, 'FFFFFF', 9)
        shade(t.rows[0].cells[i], header_fill)
    trPr = t.rows[0]._tr.get_or_add_trPr()
    tblHeader = OxmlElement('w:tblHeader')
    tblHeader.set(qn('w:val'), 'true')
    trPr.append(tblHeader)
    for ridx, row in enumerate(rows):
        cells = t.add_row().cells
        trPr = t.rows[-1]._tr.get_or_add_trPr()
        cantSplit = OxmlElement('w:cantSplit')
        trPr.append(cantSplit)
        for i, val in enumerate(row):
            set_cell_text(cells[i], val, False, DARK, 9)
            shade(cells[i], 'FFFFFF' if ridx % 2 == 0 else LIGHT)
    if widths:
        for row in t.rows:
            for i, w in enumerate(widths): row.cells[i].width = Inches(w)
    doc.add_paragraph().paragraph_format.space_after = Pt(1)
    return t


def add_heading(doc, text, level=1):
    p = doc.add_heading(text, level=level)
    p.paragraph_format.space_before = Pt(10 if level == 1 else 7)
    p.paragraph_format.space_after = Pt(4)
    return p


def add_body(doc, text, bold_prefix=None):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.12
    p.paragraph_format.space_after = Pt(5)
    if bold_prefix and text.startswith(bold_prefix):
        p.add_run(bold_prefix).bold = True
        p.add_run(text[len(bold_prefix):])
    else: p.add_run(text)
    return p


def bullet(doc, text, level=0):
    p = doc.add_paragraph(style='List Bullet' if level == 0 else 'List Bullet 2')
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.05
    p.add_run(text)
    return p


def code(doc, text):
    for line in text.strip('\n').split('\n'):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(line)
        r.font.name = 'Consolas'; r.font.size = Pt(8.5); r.font.color.rgb = RGBColor.from_string('243B53')
        shade(p._p.getparent().getparent(), 'F3F6F9') if False else None
    doc.add_paragraph().paragraph_format.space_after = Pt(1)


def checkbox(text): return '☐ ' + text


def add_page_field(p):
    r = p.add_run()
    fldChar1 = OxmlElement('w:fldChar'); fldChar1.set(qn('w:fldCharType'), 'begin')
    instrText = OxmlElement('w:instrText'); instrText.set(qn('xml:space'), 'preserve'); instrText.text = ' PAGE '
    fldChar2 = OxmlElement('w:fldChar'); fldChar2.set(qn('w:fldCharType'), 'end')
    r._r.append(fldChar1); r._r.append(instrText); r._r.append(fldChar2)


def setup(doc):
    sec = doc.sections[0]
    sec.top_margin = Inches(0.65); sec.bottom_margin = Inches(0.65)
    sec.left_margin = Inches(0.75); sec.right_margin = Inches(0.65)
    styles = doc.styles
    styles['Normal'].font.name = 'Aptos'; styles['Normal'].font.size = Pt(10.5)
    for name, size, color in [('Title', 24, NAVY), ('Heading 1', 16, NAVY), ('Heading 2', 12.5, NAVY), ('Heading 3', 11, DARK)]:
        st = styles[name]; st.font.name = 'Aptos Display' if name == 'Title' else 'Aptos'; st.font.size = Pt(size); st.font.bold = True; st.font.color.rgb = RGBColor.from_string(color)
    for sec in doc.sections:
        footer = sec.footer.paragraphs[0]
        footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
        footer.add_run('PDR TV5 – Payment Service | Trang ')
        add_page_field(footer)
        footer.runs[0].font.size = Pt(8); footer.runs[0].font.color.rgb = RGBColor.from_string('6B7280')


def build_md():
    return '''# PDR – TV5 Payment Service (Node.js)

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
'''

# Build document

doc = Document(); setup(doc)
# cover
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.space_before = Pt(32)
r=p.add_run('PDR'); r.bold=True; r.font.size=Pt(34); r.font.color.rgb=RGBColor.from_string(NAVY)
p = doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
r=p.add_run('TV5 – PAYMENT SERVICE'); r.bold=True; r.font.size=Pt(20); r.font.color.rgb=RGBColor.from_string(DARK)
p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.space_before=Pt(12)
r=p.add_run('Node.js · MongoDB · Cổng 5005'); r.font.size=Pt(13); r.font.color.rgb=RGBColor.from_string('4B5563')

table(doc, ['Thông tin', 'Giá trị'], [
    ('Dự án', 'Hệ thống đặt vé xem phim theo kiến trúc Microservices'),
    ('Vai trò', 'TV5 – Xử lý thanh toán giả lập và lưu lịch sử giao dịch'),
    ('Giữa kỳ', 'Node.js 18+ · module http · driver mongodb'),
    ('Cuối kỳ', 'Express · Mongoose · jsonwebtoken'),
    ('CSDL', 'MongoDB payment_db · collection transactions'),
    ('Tài liệu tham chiếu', 'Kế hoạch triển khai SOA Đặt vé phim v2.1, cập nhật 02/10/2026'),
], [1.7, 4.6])

p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.space_before=Pt(18)
r=p.add_run('Họ tên / MSSV: ____________________________________________'); r.font.size=Pt(11)
p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
r=p.add_run('Phiên bản PDR: 1.0  |  Ngày lập: 04/10/2026'); r.font.size=Pt(10); r.font.color.rgb=RGBColor.from_string('6B7280')

p=doc.add_paragraph(); p.paragraph_format.space_before=Pt(18); p.paragraph_format.space_after=Pt(10)
r=p.add_run('Mục tiêu tài liệu'); r.bold=True; r.font.color.rgb=RGBColor.from_string(NAVY)
add_body(doc, 'Tài liệu này chuyển yêu cầu phiếu riêng TV5 thành danh sách công việc có thể thực hiện, tiêu chí nghiệm thu, cấu trúc bàn giao và kịch bản kiểm thử. Phạm vi giữa kỳ được tách khỏi backlog cuối kỳ để bảo đảm đúng lộ trình “code thuần → framework”.')
doc.add_page_break()

add_heading(doc, '1. Tổng quan và phạm vi', 1)
add_body(doc, 'TV5 sở hữu trọn vẹn Payment Service: mô hình dữ liệu, API, sơ đồ phân tích, trang admin và báo cáo. Service nhận yêu cầu thanh toán từ Booking Service, mô phỏng kết quả, lưu giao dịch vào MongoDB và cho phép Admin xem lịch sử.')
add_body(doc, 'Phạm vi giữa kỳ: Node.js 18+, module http và driver mongodb; chưa dùng Express/Mongoose, chưa tích hợp cổng thanh toán thật và chưa bắt buộc JWT thật. Phạm vi cuối kỳ: chuyển sang Express + Mongoose, bổ sung middleware verify JWT và giới hạn GET cho ADMIN.')

table(doc, ['Hạng mục', 'Quy định phải tuân thủ'], [
    ('Cổng / bind', '5005 / 0.0.0.0 để máy khác trong nhóm có thể gọi'),
    ('CSDL', 'MongoDB payment_db; TV5 là service duy nhất sở hữu collection transactions'),
    ('FK liên service', 'bookingId là FK logic tới Booking.bookings.id; không tạo FK vật lý'),
    ('Định dạng', 'JSON; Content-Type: application/json; charset=utf-8'),
    ('CORS', 'Xử lý GET, POST, OPTIONS; OPTIONS trả 204'),
    ('HTTP chính', '201 tạo giao dịch; 200 lấy lịch sử; 400 dữ liệu/JSON sai; 405 sai method; 500 lỗi server'),
], [1.5, 4.8])

add_heading(doc, '2. Danh sách đầu ra P1–P8', 1)
table(doc, ['Mã', 'Đầu ra', 'Công việc cần hoàn thành', 'Tiêu chí nghiệm thu'], [
    ('P1', 'CSDL + seed', 'Tạo payment_db.transactions; viết seed.js chạy bằng mongosh; nạp 2 giao dịch Phụ lục A.5.', 'Có đúng các dòng (1, 180000, MOMO, PAID) và (2, 85000, VNPAY, FAILED); bookingId là Number; paidAt là Date.'),
    ('P2', 'ERD', 'Vẽ collection như một thực thể; ghi rõ kiểu dữ liệu; thể hiện FK logic.', 'Đủ 6 trường: _id:ObjectId, bookingId:Number, amount:Number, method:String, status:String, paidAt:Date.'),
    ('P3', 'Use Case', 'Actor Booking Service và Admin; xử lý, lưu, xem lịch sử.', 'Có sơ đồ và đặc tả ngắn cho 3 use case.'),
    ('P4', 'DFD mức 0/1', 'Mức 0: Booking/Admin ↔ Payment. Mức 1: tiếp nhận, xử lý/ghi, truy vấn.', 'Có kho D1 – transactions và luồng vào/ra.'),
    ('P5', 'DFD mức 2', 'Phân rã 2.0: 2.1 kiểm tra; 2.2 giả lập; 2.3 ghi; 2.4 phản hồi.', 'Thể hiện cả nhánh PAID và FAILED.'),
    ('P6', 'API', 'POST /api/payment và GET /api/payment bằng http thuần; body data/end + JSON.parse try/catch.', 'API chạy, đúng mã HTTP, lưu cả giao dịch FAILED, xử lý OPTIONS.'),
    ('P7', 'Trang admin', 'Tạo admin_payment.html; bảng 5 trường và thông báo lỗi thân thiện.', 'Gọi GET và hiển thị dữ liệu từ service.'),
    ('P8', 'Báo cáo', 'Mô tả kiến trúc, dữ liệu, API, sơ đồ, ảnh Compass, ảnh curl và hướng dẫn chạy.', 'Báo cáo có minh chứng, checklist và nêu giới hạn giữa kỳ.'),
], [0.45, 1.0, 2.75, 2.35])

add_heading(doc, '3. Thiết kế dữ liệu và seed', 1)
add_heading(doc, '3.1. Collection transactions', 2)
table(doc, ['Trường', 'Kiểu', 'Bắt buộc', 'Quy tắc / ý nghĩa'], [
    ('_id', 'ObjectId', 'Tự sinh', 'Định danh MongoDB.'),
    ('bookingId', 'Number', 'Có', 'FK logic → Booking.bookings.id; tuyệt đối không lưu chuỗi.'),
    ('amount', 'Number', 'Có', 'Số tiền VND; > 0 là nhánh PAID.'),
    ('method', 'String', 'Có', 'Chỉ MOMO, VNPAY hoặc CASH.'),
    ('status', 'String', 'Có', 'Chỉ PAID hoặc FAILED.'),
    ('paidAt', 'Date', 'Có', 'Thời điểm xử lý, dùng Date/ISODate.'),
], [1.0, 0.9, 0.8, 4.0])
add_body(doc, 'Ghi chú nhất quán dữ liệu: Payment Service không tạo khóa ngoại thật sang booking_db. Booking Service chịu trách nhiệm truyền bookingId hợp lệ; TV5 lưu dạng Number để khớp với bookings.id.')
add_heading(doc, '3.2. Dữ liệu seed bắt buộc theo Phụ lục A.5', 2)
code(doc, '''use payment_db;
db.transactions.deleteMany({});
db.transactions.insertMany([
  { bookingId: 1, amount: 180000, method: "MOMO",  status: "PAID",   paidAt: ISODate("2026-10-01T10:00:00Z") },
  { bookingId: 2, amount: 85000,  method: "VNPAY", status: "FAILED", paidAt: ISODate("2026-10-01T10:05:00Z") }
]);''')
bullet(doc, 'Lưu file tại seed/payment_seed.js hoặc payment-service/seed.js; chạy bằng mongosh, không phải node seed.js.')
bullet(doc, 'Sau khi seed, mở MongoDB Compass, chọn payment_db → transactions và chụp ảnh đủ các trường để đưa vào P8.')
bullet(doc, 'Không đổi bookingId, amount, method, status của hai giao dịch mẫu; paidAt có thể dùng thời điểm cố định để ảnh minh chứng tái lập được.')

add_heading(doc, '4. Đặc tả Use Case và DFD', 1)
table(doc, ['Use Case', 'Actor', 'Tiền điều kiện', 'Kết quả'], [
    ('UC1 – Xử lý thanh toán', 'Booking Service', 'Có bookingId, amount, method.', 'Tạo giao dịch PAID nếu hợp lệ; FAILED nếu amount ≤ 0 hoặc method sai.'),
    ('UC2 – Lưu giao dịch', 'Payment Service', 'Đã xác định status và paidAt.', 'Insert vào D1 – transactions; trả giao dịch đã lưu.'),
    ('UC3 – Xem lịch sử', 'Admin', 'Payment Service đang chạy.', 'GET trả mảng giao dịch; admin hiển thị trong bảng.'),
], [1.55, 1.1, 2.3, 2.0])
add_body(doc, 'Yêu cầu sơ đồ: DFD0 thể hiện Booking Service và Admin trao đổi với Payment Service. DFD1 gồm 1.0 Tiếp nhận yêu cầu thanh toán, 2.0 Xử lý và ghi giao dịch, 3.0 Truy vấn lịch sử và kho D1 transactions. DFD2 phân rã 2.0 thành 2.1 Kiểm tra số tiền/phương thức, 2.2 Giả lập cổng thanh toán, 2.3 Ghi giao dịch, 2.4 Tạo phản hồi.')

add_heading(doc, '5. Đặc tả API giữa kỳ', 1)
table(doc, ['Method & URL', 'Request', 'Xử lý', 'Response kỳ vọng'], [
    ('POST /api/payment', '{ bookingId, amount, method }', 'Validate; hợp lệ → PAID; sai → FAILED; luôn insert.', '201 + giao dịch đã lưu.'),
    ('GET /api/payment', 'Không có body', 'Đọc transactions; nên sắp xếp paidAt giảm dần.', '200 + mảng giao dịch.'),
    ('OPTIONS /api/payment', 'Preflight', 'Trả CORS headers.', '204, không body.'),
], [1.35, 1.75, 2.75, 1.45])
add_heading(doc, '5.1. Quy tắc xử lý body và lỗi', 2)
bullet(doc, 'Dùng req.on("data", ...) để nối chuỗi body và req.on("end", ...) để JSON.parse trong try/catch.')
bullet(doc, 'JSON sai cú pháp phải trả 400 và không được làm sập tiến trình Node.js.')
bullet(doc, 'method hợp lệ là MOMO, VNPAY, CASH; nên chuẩn hóa bằng String(method).toUpperCase() nhưng phải ghi rõ trong báo cáo.')
bullet(doc, 'amount phải là Number và lớn hơn 0. amount ≤ 0 hoặc method không hợp lệ vẫn được lưu với status FAILED.')
bullet(doc, 'Cấu trúc trả về nên thống nhất với nhóm: { "status": "success", "data": ... } hoặc thông báo lỗi { "status": "error", "message": "..." }.')
add_heading(doc, '5.2. Ví dụ request và curl', 2)
code(doc, '''curl -X POST http://localhost:5005/api/payment \\
  -H "Content-Type: application/json" \\
  -d '{"bookingId":3,"amount":180000,"method":"MOMO"}'

curl http://localhost:5005/api/payment

# Nhánh FAILED: amount không hợp lệ
curl -X POST http://localhost:5005/api/payment \\
  -H "Content-Type: application/json" \\
  -d '{"bookingId":3,"amount":0,"method":"MOMO"}'

# Nhánh FAILED: method không hợp lệ
curl -X POST http://localhost:5005/api/payment \\
  -H "Content-Type: application/json" \\
  -d '{"bookingId":3,"amount":180000,"method":"BANK"}' ''')

add_heading(doc, '6. Kế hoạch cấu trúc mã nguồn và admin', 1)
code(doc, '''payment-service/
├── payment_service.js       # server module http, router, API handlers
├── seed.js                   # seed chạy bằng mongosh (hoặc file seed/payment_seed.js)
├── package.json
├── config.example            # MONGO_URI, PORT, JWT_SECRET cho cuối kỳ
├── .gitignore
└── admin_payment.html        # bảng lịch sử giao dịch''')
table(doc, ['Thành phần', 'Việc cần làm', 'Hoàn thành khi'], [
    ('Server', 'Listen 0.0.0.0:5005; route theo method + pathname.', 'node payment_service.js khởi động không lỗi.'),
    ('MongoDB', 'Connect payment_db; insert/find transactions.', 'Compass thấy dữ liệu và API đọc được.'),
    ('Validation', 'Kiểm tra bookingId, amount, method; gán PAID/FAILED.', 'Có test hợp lệ, amount ≤ 0 và method sai.'),
    ('CORS', 'Headers cho Origin/Methods/Headers; OPTIONS 204.', 'Admin gọi API không bị chặn preflight.'),
    ('Admin', 'Fetch GET; render bảng bookingId, tiền VND, phương thức, trạng thái, thời gian.', 'Có empty state và thông báo service chưa chạy.'),
], [1.1, 3.5, 2.1])

add_heading(doc, '7. Kiểm thử và minh chứng', 1)
table(doc, ['ID', 'Kịch bản', 'Input / thao tác', 'Kỳ vọng'], [
    ('T01', 'PAID – MOMO', 'bookingId=3, amount=180000, method=MOMO', '201; status PAID; lưu Number/Date.'),
    ('T02', 'PAID – VNPAY', 'bookingId=4, amount=85000, method=VNPAY', '201; status PAID.'),
    ('T03', 'FAILED – amount 0', 'amount=0, method=MOMO', 'FAILED; vẫn có bản ghi trong DB.'),
    ('T04', 'FAILED – amount âm', 'amount=-1, method=CASH', 'FAILED; vẫn có bản ghi.'),
    ('T05', 'FAILED – method sai', 'method=BANK', 'FAILED; vẫn có bản ghi.'),
    ('T06', 'JSON hỏng', 'Body {"bookingId":', '400; server vẫn chạy.'),
    ('T07', 'GET history', 'curl GET /api/payment', '200; body là mảng giao dịch.'),
    ('T08', 'CORS preflight', 'curl -X OPTIONS /api/payment', '204 và đủ headers CORS.'),
], [0.45, 1.55, 2.75, 2.0])
add_body(doc, 'Ảnh cần đưa vào báo cáo: (1) terminal chạy server, (2) curl POST nhánh PAID, (3) curl POST nhánh FAILED, (4) curl GET, (5) MongoDB Compass hiển thị hai seed và các giao dịch test, (6) trang admin.')

add_heading(doc, '8. Phân công, mốc hoàn thành và bàn giao', 1)
table(doc, ['Mốc', 'Việc TV5', 'Sản phẩm bàn giao'], [
    ('M1 – Chuẩn bị', 'Tạo DB, collection, seed; hoàn thiện ERD nháp.', 'seed.js, ảnh Compass, ERD nguồn + PNG.'),
    ('M2 – API core', 'Implement http, body parser, validation, insert/find, CORS.', 'payment_service.js chạy cổng 5005.'),
    ('M3 – Admin + test', 'Làm admin_payment.html; chạy T01–T08; chụp minh chứng.', 'admin_payment.html, log/curl, ảnh kiểm thử.'),
    ('M4 – Hồ sơ', 'Viết Use Case, DFD0/1/2, báo cáo P8; rà checklist.', 'docs/tv5-payment/ đầy đủ P1–P8.'),
    ('M5 – Ghép nhóm', 'Bàn giao hợp đồng endpoint cho TV4/TV6; hỗ trợ tab admin.', 'URL, request/response, CORS, dữ liệu seed và lưu ý tích hợp.'),
], [1.25, 3.55, 1.95])
add_body(doc, 'Đề xuất cấu trúc repo theo kế hoạch chung: docs/tv5-payment/, payment-service/, seed/payment_seed.js; tên sơ đồ: ERD_payment.png, UC_payment.png, DFD0_payment.png, DFD1_payment.png, DFD2_payment.png và lưu kèm file nguồn draw.io.')

add_heading(doc, '9. Backlog cuối kỳ', 1)
bullet(doc, 'Chuyển HTTP router sang Express và MongoDB driver sang Mongoose model/schema.')
bullet(doc, 'Thêm middleware verify JWT bằng jsonwebtoken; GET /api/payment chỉ cho role ADMIN.')
bullet(doc, 'Giữ nguyên hợp đồng POST /api/payment để Booking Service có thể gọi; Booking chuyển tiếp Authorization token.')
bullet(doc, 'Bổ sung timeout/error handling khi Booking gọi Payment; không làm mất trạng thái đơn khi Payment hoặc Notification lỗi.')
bullet(doc, 'Thêm test tự động, logging, biến môi trường và tài liệu triển khai.')

add_heading(doc, '10. Checklist tự kiểm tra trước khi nộp', 1)
for item in [
    'P1: payment_db và transactions tạo đúng; seed A.5 chạy bằng mongosh.',
    'P2: ERD ghi rõ ObjectId, Number, String, Date và FK logic bookingId.',
    'P3: Use Case có Booking Service, Admin và 3 use case chính.',
    'P4: DFD mức 0 và mức 1 có D1 – transactions.',
    'P5: DFD mức 2 có 2.1–2.4 và hai nhánh PAID/FAILED.',
    'P6: POST/GET chạy trên 0.0.0.0:5005; xử lý body data/end, JSON.parse try/catch, OPTIONS.',
    'P7: admin_payment.html hiển thị đủ bookingId, amount, method, status, paidAt.',
    'P8: Báo cáo có hướng dẫn chạy, ảnh Compass, ảnh curl và ghi rõ giới hạn giữa kỳ.',
    'bookingId được lưu dạng Number; không để lộ mật khẩu hoặc khóa bí mật trong repo.',
]:
    bullet(doc, checkbox(item))

add_heading(doc, '11. Kết luận', 1)
add_body(doc, 'Hoàn thành PDR này đồng nghĩa TV5 có một Payment Service độc lập, có dữ liệu mẫu tái lập được, API đúng hợp đồng nhóm, sơ đồ phân tích đủ P3–P5, trang admin và bộ minh chứng P6–P8. Điểm cần ưu tiên kiểm tra là nhánh FAILED vẫn phải được lưu, bookingId phải là Number và server http thuần phải tự xử lý body/JSON an toàn.')

# save markdown and docx
MD.write_text(build_md(), encoding='utf-8')
doc.save(DOCX)
print(DOCX)
print(MD)
