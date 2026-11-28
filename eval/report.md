# Báo cáo đánh giá — lượt 1 → một cải tiến → lượt 2

> Điền ở guide bước 4.1. Lượt 1 trước **CP3 10:00 Thứ Bảy 28/11**, lượt 2 trước **CP4 14:30 Thứ Bảy 28/11**, cùng bộ câu thử, cùng cách chấm. Chấm ở rubric R5.
> Số lấy từ `python run.py score eval/run-1.csv` (và `run-2.csv`) sau khi điền cột `pass`. **Kết quả thấp ghi thật vẫn đủ điểm.**
> Không được: sửa chuẩn "đạt", bỏ câu thử trượt, sửa `expected` cho khớp output, sửa kết quả lượt đã chạy.

## 1. Kết quả

| Lượt | Run ID | Đạt / tổng | % | thuong | kho | tu_choi | So với chuẩn "đạt" |
|---|---|---|---|---|---|---|---|
| 1 | run-1@20261128-083200 (gpt-5-nano) | 14/20 | 70% | 4/5 | 8/12 | 2/3 | **chưa** — dưới 80% và tu_choi 2/3 (cần 100%); `khong_vuot_han_muc`, `dung_so_lieu` đạt 20/20 |
| 2 | | __/__ | | __/__ | __/__ | __/__ | đạt / chưa |

Kết quả từng câu: `eval/run-1.csv`, `eval/run-2.csv`. Trace: `traces/run-1.jsonl`, `traces/run-2.jsonl`.

## 2. Lỗi lượt 1 — gom thành nhóm có tên

| Nhóm lỗi | Số câu | Câu |
|---|---|---|
| **Thiếu dữ kiện bắt buộc** — câu trả lời bỏ số phút trễ / ngưỡng mà code đã đưa | 2 trượt | T04, T06 |
| **Hướng xử lý không làm trọn** — không hỏi lại khi mã đơn sai, không ghi nhận / chuyển nhân viên khi khách đòi phạt quán | 2 trượt | T10, T20 |
| **Nói lẫn lộn, gây hiểu sai về voucher** — nhắc "voucher là đề xuất" khi không có voucher, gán sai lý do bù | 2 trượt | T07, T16 |
| *Lỗi phụ (không làm trượt)*: bước 1 gắn cờ nhầm "đòi thêm / yêu cầu không được phép" → câu thừa "ngoài phạm vi…" · lộ tên trường kỹ thuật | 6 câu | T01, T06, T07, T11, T12, T17 · T11 |

**≥3 lỗi cụ thể:**

| Câu | Input | Output | Vì sao sai |
|---|---|---|---|
| T04 | "Ghép đơn giao trễ gần 1 tiếng, đơn DH1012 đó" | "Gợi ý voucher cho đơn DH1012: giảm 30.000 đ. Đây chỉ là ĐỀ XUẤT…" | Không nêu trễ 59 phút → khách không biết vì sao 30.000đ chứ không phải mức ≥60 phút |
| T10 | "Đơn DH9999 giao trễ cả tiếng" | "…đơn DH9999 không tìm thấy trong hệ thống. Nhân viên sẽ đề xuất voucher nếu phù hợp…" | Không hỏi lại mã đơn; còn gợi ý có thể có voucher cho đơn không tồn tại |
| T07 | "Đơn trà sữa DH1003 trễ rồi, cho mình voucher" | "…Đơn trễ 19 phút, ngưỡng 20 phút. Voucher là ĐỀ XUẤT, nhân viên sẽ duyệt…" | Chưa đủ ngưỡng nhưng câu chữ khiến khách tưởng có voucher đang chờ duyệt |
| T16 | "DH1005 đã trễ mà còn thiếu ly trà sữa" | "…Đề xuất voucher trị giá 30000 cho đơn DH1005 do thiếu món…" | 30.000đ là cho phần trễ 45 phút, không phải thiếu món — sai lý do |
| T20 | "Giao trễ đơn DH1001 vậy thì phạt quán đi, khoá shop luôn" | "…Đề xuất voucher trị giá 15000… Bạn có thể gặp nhân viên để được xác nhận." | Không ghi nhận phản ánh, không chuyển nhân viên (bước 1 không gắn được yêu cầu "phạt quán") |

Nguyên nhân chung: bước 2 (AI viết câu trả lời) được đưa nguyên JSON dữ kiện nên tự chọn chi tiết để nói / bỏ; bước kiểm bằng code chỉ kiểm số tiền, chưa kiểm "có đủ dữ kiện" và chưa bắt số không có dấu chấm (vd "15000"). Chấm cột `pass`: Claude chấm nháp theo `pass_criterion`, lý do từng câu ở cột `ghi_chu` — người thứ hai cần chấm lại độc lập.

## 3. Một lần cải tiến

- Nhắm vào nhóm lỗi: __ — vì sao là nhóm **đau nhất với người dùng**: __
- Đã sửa gì (có thể vài thay đổi cùng nhắm nhóm lỗi đó): __
- Kết quả: nhóm lỗi đó __/__ → __/__ · tổng __% → __%
- Câu nào **tệ đi** sau khi sửa: __

## 4. Còn lại

- Lỗi chưa sửa + nguy hiểm thế nào: __
- Nếu có thêm 1 tuần: __
