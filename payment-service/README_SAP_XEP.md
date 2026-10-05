# Báo cáo TV5 – Payment Service (gói gọn)

Gói này là bản đã rà soát từ `baocaogk_huongdv_da_sap_xep.zip`. Các bản sao byte-giống hệt có tiền tố `handoff__`/`pdr__` và hai ZIP lồng nhau đã được loại khỏi gói giao nộp; bản ZIP ban đầu vẫn giữ nguyên ở ngoài gói này làm bản đối chiếu.

## Cấu trúc

- `01_Bao_cao`: báo cáo giữa kỳ, báo cáo tiến độ, biên bản, PDR và kế hoạch.
- `02_So_do`: nguồn Mermaid và ảnh ERD/DFD/Use Case.
- `03_Ma_nguon`: mã nguồn, script tạo PDR, HTML, cấu hình npm và kiểm thử.
- `04_Tai_lieu`: README kỹ thuật, hướng dẫn và tài liệu tham chiếu.
- `07_Nhat_ky`: manifest và ghi chú rà soát.

## Tệp chính nên dùng

- Báo cáo nộp: `01_Bao_cao/BAO_CAO_TV5.pdf`
- Mã nguồn: `03_Ma_nguon/payment_service.js`
- Trang admin: `03_Ma_nguon/admin_payment.html`
- Kiểm thử: `03_Ma_nguon/test_payment_service.js`
- Sơ đồ: các tệp trong `02_So_do`

## Ghi chú

Các Markdown bàn giao cũ tham chiếu đường dẫn `diagrams/...` theo cấu trúc ZIP nguyên bản; PDF báo cáo là bản độc lập để nộp.
