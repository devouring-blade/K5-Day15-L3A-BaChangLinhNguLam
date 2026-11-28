# Data card — dữ liệu bản chạy thử dùng

> Bản đầu CP2 (27/11/2026). Dữ liệu chạy thử nằm trong `data/`. Data `synthetic` **không phải bằng chứng pain** — bằng chứng ở `evidence/`.

## Dataset 1 · Đơn hàng giả — `data/don_hang.csv`

| | |
|---|---|
| Dùng để làm gì | nguồn cho công cụ `get_order` · đáp án của bộ câu thử `eval/benchmark.csv` |
| Từ đâu | nhóm tự viết tay; tên quán dựng ("Quán Mẫu …"), mã đơn / mã khách dựng |
| Xử lý những bước gì | không — viết tay; mỗi đơn chọn để phủ một ca: trễ 12 / 19 / 20 / 35 / 45 / 59 / 62 / 75 phút, giao sớm, đơn huỷ, đơn giá trị cao (300.000đ) |
| Số dòng / số đoạn | 12 đơn |
| Phiên bản / ngày lấy | v1 · 27/11/2026 |
| Nhãn | `synthetic` |
| Giới hạn | không có đơn nhiều món, không có giờ quán nhận / tài xế nhận; giờ là giờ Việt Nam, không múi giờ. Không có dữ liệu thật của ai |

**Cách sinh:** viết tay, không dùng seed. Người kiểm: __ · số dòng đã kiểm tay: __/12 (đối chiếu số phút trễ với `eval/benchmark.csv`).

## Dataset 2 · Chính sách bù giao trễ — `data/chinh_sach.csv`

| | |
|---|---|
| Dùng để làm gì | nguồn cho công cụ `get_policy` và `compute_delay_compensation` (code tính mức bù) |
| Từ đâu | **nhóm tự đặt** — mốc phút trễ và mức voucher. Tham khảo cấu trúc từ chương trình "Giao nhanh đúng hẹn" của sàn Shopee (https://help.shopee.vn/portal/4/article/147164, xem 28/11/2026): trễ → 1 voucher, loại trừ đơn huỷ và trễ do người mua; trang này ghi rõ **không áp dụng cho ShopeeFood** và không công bố giá trị voucher → các mức tiền là tự đặt |
| Xử lý những bước gì | viết tay thành bảng: `< 20 phút` → 0 · `20–39` → 15.000đ · `40–59` → 30.000đ · `≥ 60` → 50.000đ · hạn mức tự động 50.000đ · danh sách ca chuyển nhân viên |
| Số dòng / số đoạn | 6 dòng |
| Phiên bản / ngày lấy | v1 · 27/11/2026 |
| Nhãn | `synthetic` (tự đặt) |
| Giới hạn | không phải chính sách thật của app nào; mức bù thật có thể khác hoặc không công bố |

## Dataset 3 · Lịch sử khiếu nại giả — `data/lich_su_khieu_nai.csv`

| | |
|---|---|
| Dùng để làm gì | nguồn cho công cụ `get_complaint_history` (khách ≥3 khiếu nại trễ / 30 ngày → chuyển nhân viên) |
| Từ đâu | nhóm tự viết tay |
| Xử lý những bước gì | không |
| Số dòng / số đoạn | 10 khách |
| Phiên bản / ngày lấy | v1 · 27/11/2026 |
| Nhãn | `synthetic` |
| Giới hạn | chỉ đếm số lần, không có nội dung / kết quả khiếu nại cũ |

## Dataset 4 · Bộ câu thử — `eval/benchmark.csv`

| | |
|---|---|
| Dùng để làm gì | đo bản chạy thử (`python run.py eval`) |
| Từ đâu | 9/20 câu viết lại từ lời người dùng thật (`nguoi_dung`: phiếu khảo sát #1, #2, #3, #6, #17, #20, #23) và review thật (`data_that`: review #26, #53), gắn mã đơn giả; 11/20 câu nhóm tự viết theo kịch bản `spec.md` §5 |
| Xử lý những bước gì | viết lại câu chữ, bỏ mọi chi tiết nhận ra người viết; đáp án tính từ Dataset 1 + 2 |
| Số dòng / số đoạn | 20 câu · thuong 5 · kho 12 · tu_choi 3 (gồm 2 câu tấn công) |
| Phiên bản / ngày lấy | v1 · 27/11/2026 (chốt CP2) |
| Nhãn | thật (ý) + `synthetic` (mã đơn) |
| Giới hạn | toàn tiếng Việt có dấu / không dấu ít; chưa có câu nhiều đơn trong một tin |
