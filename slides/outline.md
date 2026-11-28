# Dàn slide → lấy số từ file nào

> Làm ở guide bước 5.1. Luật: **không có bằng chứng thì không có slide** — mỗi trang ≥1 con số / trích dẫn có nguồn / kết quả đo.
> Xuất PDF thành `demo-slides.pdf` ở thư mục gốc repo (nguồn: `slides/demo-slides.html`, xuất bằng Edge headless), nộp tại CP4 14:30 Thứ Bảy 28/11. Nộp PDF, không nộp link.

| # | Trang | Có gì | Số lấy từ | Xong |
|---|---|---|---|---|
| 1 | Người dùng & pain | Ai · việc gì · chỗ đau + số và trích dẫn | `evidence/summary.md` | ☑ |
| 2 | Vì sao chọn bài này | Bảng impact rút gọn + hướng bị loại | `spec.md` §2 | ☑ |
| 3 | Giải pháp | Lát cắt một câu · sơ đồ · AI tự làm đến đâu, vì sao | `spec.md` §4 | ☑ |
| 4 | Demo live | 1 trường hợp thường + 1 trường hợp khó (lấy từ bộ câu thử); mạng hỏng → video dự phòng | `eval/benchmark.csv` | ☑ |
| 5 | **Đánh giá thế nào** | Dataset · bộ câu thử · metric · lượt 1 → lượt 2 so với chuẩn "đạt" (kèm run ID) · lỗi chính | `eval/README.md`, `eval/report.md` | ☑ |
| 6 | **Chi phí khi dùng thật** | Chi phí / task thành công · 3 kịch bản · so với impact | `cost/cost-estimate.md` | ☑ |
| 7 | Kết luận | Go / iterate / stop — dẫn số ở trang 1, 5, 6 | — | ☑ |
| 8 | Nếu có thêm 1 tuần | 2–3 việc, trỏ về lỗi còn lại / phản hồi người dùng | `eval/report.md` mục 4 · `validation/log.md` | ☑ |

**Trước khi lên:** tải repo về một máy khác (hoặc thư mục mới), chạy theo mục "Chạy trong 3 phút" của `README.md` · `.env` có trên máy demo, đã gọi thử 1 câu trong vòng 1 giờ trước giờ demo · video dự phòng mở được bằng cửa sổ ẩn danh · biết bản chạy thử sẽ làm gì với **1 câu thử lạ** của giám khảo.

Ai nói trang nào (mỗi người ≥1 phần):

| Trang | Người nói |
|---|---|
| 1 · Người dùng & pain | Lê Minh Phụng (làm khảo sát) |
| 2 · Vì sao chọn bài này | Đào Trường Vũ (đào review) |
| 3 · Giải pháp | Nguyễn Sỹ Huy Kiên (bản chạy thử) |
| 4 · Demo live | Nguyễn Sỹ Huy Kiên — gõ lệnh; Vũ Lê Hoàng đọc câu thử |
| 5 · Đánh giá thế nào | Vũ Lê Hoàng (câu thử, data) |
| 6 · Chi phí khi dùng thật | Đào Trường Vũ (mô phỏng chi phí) |
| 7 · Kết luận | Lê Minh Phụng |
| 8 · Nếu có thêm 1 tuần | Vũ Lê Hoàng |

## Phao hỏi đáp — giám khảo hỏi BẤT KỲ AI (rubric R7)

**Ai cũng phải trả lời được 4 câu:**

1. **Vì sao chọn workflow, không chọn agent?** Các bước luôn giống nhau (đọc tin → tra đơn → tính bù → kiểm), nên workflow rẻ và dễ đo. Để AI tự gọi công cụ thì dễ bỏ bước kiểm hạn mức. Không có vai nào khác nhau nên không cần nhiều agent. (`spec.md` §4)
2. **Lỗi nguy hiểm nhất là gì?** Bù sai tiền / vượt hạn mức (khách nài, doạ, chèn lệnh) → chặn bằng: tiền chỉ tính bằng code (`compute_delay_compensation`), code kiểm số tiền sau AI, mọi voucher là bản nháp nhân viên duyệt. Ca nguy hiểm cho người: khách báo đau bụng sau khi ăn → dừng bù, chuyển nhân viên ngay (T15).
3. **Chi phí / task thành công tính thế nào?** Chạy thật 50 phiên giả lập theo 3 persona từ khảo sát → đo token thật → nhân giá model → chia tỉ lệ đạt (20/20 lượt 3). gpt-5-nano ≈ $0,00081 ≈ 21 ₫. Chi phí lớn thật là voucher và giờ công duyệt, không phải model. (`cost/cost-estimate.md`)
4. **Phần mình làm là gì?** Xem bảng dưới — nói đúng file có tên mình.

**Từng người chuẩn bị thêm:**

| Người | Phần mình (TEAMS.md) | Câu dễ bị hỏi + ý trả lời |
|---|---|---|
| Nguyễn Sỹ Huy Kiên | `codebase/` — agent, tools, nối model | *AI quyết định gì, code quyết định gì?* AI đọc tin (mã đơn, vấn đề, đòi thêm, yêu cầu cấm) và viết câu trả lời; code tính phút trễ, mức bù, chọn hướng, kiểm số tiền. · *Lượt 2 có gì lạ?* Hàm bắt số tiền bắt nhầm mã đơn DH1001 → mọi câu AI viết bị loại; sửa và chạy lượt 3. · *Câu thử lạ thì sao?* Không có mã đơn → hỏi lại; mã không có → nói không tìm thấy; số tiền luôn từ code. |
| Lê Minh Phụng | Khảo sát + `evidence/summary.md` | *Khảo sát hỏi ai, bao nhiêu người?* 23 phiếu, 21 người có đặt đơn, ngoài nhóm, ẩn danh, hỏi "5 đơn gần nhất". · *Review và khảo sát lệch nhau chỗ nào?* Khảo sát thấy thiếu món cũng nhiều (65%), review thì gần như không — vì review chấm app, người thiếu món xử lý với quán. Giao trễ khớp ở cả hai. |
| Vũ Lê Hoàng | `data/`, `eval/benchmark.csv` | *Data từ đâu?* 12 đơn giả viết tay phủ đủ ca trễ 12→75 phút, đơn huỷ, đơn 300k; chính sách tự đặt, tham khảo "Giao nhanh đúng hẹn" của Shopee. · *Vì sao tin được 20/20?* Tiêu chí kiểm được, người thứ hai chấm lại 5/5; nhưng bộ câu nhỏ, nhóm biết trước → cần câu thử lạ. |
| Đào Trường Vũ | Review + `cost/` | *Đếm review thế nào?* 150 review mới nhất, mọi mức sao, mẫu số 150, nhãn định nghĩa trước, script `evidence/count_reviews.py`, người thứ hai khớp 30/30. · *Quy mô 10.000 / 100.000 lấy đâu?* Tự ước tính, ghi rõ; mức có nguồn là 910 người (khoá AI20K). |

