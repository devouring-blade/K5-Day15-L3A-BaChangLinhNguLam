# Báo cáo đánh giá — lượt 1 → một cải tiến → lượt 2

> Điền ở guide bước 4.1. Lượt 1 trước **CP3 10:00 Thứ Bảy 28/11**, lượt 2 trước **CP4 14:30 Thứ Bảy 28/11**, cùng bộ câu thử, cùng cách chấm. Chấm ở rubric R5.
> Số lấy từ `python run.py score eval/run-1.csv` (và `run-2.csv`) sau khi điền cột `pass`. **Kết quả thấp ghi thật vẫn đủ điểm.**
> Không được: sửa chuẩn "đạt", bỏ câu thử trượt, sửa `expected` cho khớp output, sửa kết quả lượt đã chạy.

## 1. Kết quả

| Lượt | Run ID | Đạt / tổng | % | thuong | kho | tu_choi | So với chuẩn "đạt" |
|---|---|---|---|---|---|---|---|
| 1 | run-1@20261128-083200 (gpt-5-nano) | 14/20 | 70% | 4/5 | 8/12 | 2/3 | **chưa** — dưới 80% và tu_choi 2/3 (cần 100%); `khong_vuot_han_muc`, `dung_so_lieu` đạt 20/20 |
| 2 | run-2@20261128-090611 (gpt-5-nano) | 20/20 | 100% | 5/5 | 12/12 | 3/3 | đạt — **nhưng mọi câu trả lời là câu mẫu từ code** (lỗi bước kiểm, xem §3) |
| 5 *(sau CP4: form xác nhận + tự duyệt bằng luật code)* | run-5@20261128-143157 (gpt-5-nano) | 20/20 | 100% | 5/5 | 12/12 | 3/3 | đạt — chỉ ghi nhận, không dùng để chấm R5 |
| 4 *(bản demo: lời nói trực tiếp với khách, trước CP4)* | run-4@20261128-141120 (gpt-5-nano) | 20/20 | 100% | 5/5 | 12/12 | 3/3 | đạt — lỗi phụ câu lặp / mục rỗng (T06, T18–T20) đã sửa sau lượt, chưa chạy lại |
| 3 *(chạy thêm sau khi sửa lỗi bước kiểm, trước CP4)* | run-3@20261128-091039 (gpt-5-nano) | 20/20 | 100% | 5/5 | 12/12 | 3/3 | **đạt** — 15/20 câu do AI viết, 5 câu hỏi lại / chuyển nhân viên dùng câu mẫu theo thiết kế |

Kết quả từng câu: `eval/run-1.csv`, `eval/run-2.csv`, `eval/run-3.csv`. Trace: `traces/run-1.jsonl`, `traces/run-2.jsonl`, `traces/run-3.jsonl`. Cột `pass` do Claude chấm nháp (lý do ở `ghi_chu`); lượt 1 có người thứ hai chấm lại 5 câu, khớp 5/5.

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

- Nhắm vào nhóm lỗi: **câu trả lời không khớp quyết định của code** — thiếu dữ kiện (T04, T06), nói gây hiểu sai về voucher / sai lý do (T07, T16), không làm trọn hướng xử lý (T10, T20) — vì sao là nhóm **đau nhất với người dùng**: pain chính là khách "không biết có được bù gì" (13/16 lần trễ không được bù / không khiếu nại, `evidence/summary.md`); nói thiếu hoặc nói sai mức bù làm hỏng đúng chỗ đó.
- Đã sửa gì (`codebase/agent.py`):
  1. Code soạn sẵn **ý bắt buộc** (số phút trễ, ngưỡng, mức bù, lý do "phần trễ X phút") — AI chỉ viết lại cho tự nhiên, không nhận JSON thô nữa.
  2. Bước kiểm bằng code thêm: đủ dữ kiện bắt buộc theo hành động; không nhắc voucher khi chưa đủ điều kiện / chưa có đơn; bắt cả số tiền viết liền ("15000", "15k").
  3. Hỏi lại / chuyển nhân viên dùng câu mẫu của code (không cần AI viết, tránh nói sai).
  4. Câu về phần ngoài phạm vi do code thêm, chỉ khi thật sự có; yêu cầu bị cấm (phạt quán, xin số điện thoại…) → ghi nhận phản ánh + chuyển nhân viên. Prompt bước 1 thêm định nghĩa `doi_them`, `yeu_cau_cam`.
- Kết quả: nhóm lỗi đó 0/6 → 6/6 · tổng 70% → 100% (lượt 2) → 100% (lượt 3).
- **Lượt 2 có lỗi của chính bước kiểm:** hàm bắt số tiền bắt nhầm mã đơn (DH**1001** → "1001 đồng"), nên **mọi câu AI viết bị loại**, 20/20 câu lượt 2 là câu mẫu từ code (trace: "số tiền [1001] không khớp mức code tính"). Kết quả lượt 2 đúng với tiêu chí nhưng không đo được câu AI viết. Đã sửa (bỏ số dính chữ) và **chạy thêm lượt 3** trước CP4: 15/20 câu do AI viết, vẫn 20/20.
- Câu nào **tệ đi** sau khi sửa: không câu nào trượt; nhưng câu AI viết ở lượt 3 gần như chép nguyên ý bắt buộc (cứng, có chỗ xưng "khách" thay vì "bạn", T02 giữ gạch đầu dòng) — đổi lại độ chính xác.

## 4. Còn lại

- Lỗi chưa sửa + nguy hiểm thế nào: bước 1 đôi khi gắn nhầm "đòi thêm" → câu thừa "nếu muốn mức bù cao hơn…" ngay cả khi không có bù (T06, T11) — không sai tiền nhưng gây khó hiểu; câu mẫu chuyển nhân viên cho ca sức khoẻ (T15) đọc như ghi chú nội bộ — ca nguy hiểm nhất cần lời khuyên rõ hơn; bộ câu thử chỉ 20 câu, 20/20 có thể là do câu thử còn dễ với luồng có code kiểm.
- Nếu có thêm 1 tuần: thêm câu thử mới chưa từng thấy (nhiều đơn trong một tin, tiếng lóng, không dấu) để đo lại; viết lại câu mẫu ca sức khoẻ; đo tỉ lệ AI gắn nhầm `doi_them`; thử chính sách thật nếu app công bố.
