# Khảo sát — bộ câu hỏi và cách gửi

- Công cụ: Google Form, tạo bằng `evidence/survey/create_form.gs` (bộ câu hỏi dưới đây giống hệt script).
- Người trả lời: người đặt đồ ăn qua app, **ngoài nhóm**. Không thu tên, email, số điện thoại.
- Kênh gửi: __ · giờ mở: 27/11/2026 ~18:07 · giờ chốt: 27/11/2026 ~19:10 · số người trả lời: 23 phiếu (21 người có đặt đồ ăn qua app, 2 phiếu kết thúc sớm)
- Kết quả: `evidence/survey/results.csv` (bản đã xoá cột Timestamp và mọi cột nhận ra người trả lời).

## Câu hỏi

**Phần 1 — Thói quen**
1. Bạn là: Sinh viên · Đi làm · Khác
2. Bạn hay đặt đồ ăn qua app nào nhất? ShopeeFood · GrabFood · BeFood · Xanh SM Ngon · App khác · Không đặt đồ ăn qua app (→ kết thúc)
3. Trung bình mỗi tuần bạn đặt bao nhiêu đơn đồ ăn qua app? 0 (→ kết thúc) · 1–2 · 3–5 · 6–10 · Trên 10

**Phần 2 — 5 đơn gần nhất**
4. Trong 5 đơn gần nhất, có mấy đơn bị GIAO TRỄ (đến muộn hơn giờ app dự kiến từ 15 phút trở lên)? 0 (→ Phần 4) · 1 · 2 · 3 · 4 · 5 · Không nhớ
5. Trong 5 đơn gần nhất, có mấy đơn bị THIẾU hoặc SAI MÓN? 0 · 1 · 2 · 3 · 4 · 5 · Không nhớ

**Phần 3 — Lần giao trễ gần nhất**
6. Lần giao trễ gần nhất, đơn đến muộn khoảng bao lâu so với dự kiến? 15–30 phút · 30–60 phút · Trên 60 phút · Không nhớ
7. Lúc đó bạn đã làm gì? (chọn nhiều) Khiếu nại trong app · Nhắn/gọi shipper · Nhắn/gọi quán · Huỷ đơn · Bỏ qua, chờ tiếp · Khác
8. Bạn có được bù gì không? Voucher · Hoàn tiền một phần · Hoàn tiền toàn bộ · Không được gì · Không khiếu nại nên không biết
9. Nếu đã khiếu nại: mất bao lâu từ lúc khiếu nại đến khi có kết quả? Dưới 5 phút · 5–30 phút · Vài giờ · Hơn 1 ngày · Không có kết quả · Không khiếu nại
10. Nếu không khiếu nại, vì sao? Không biết có được bù không · Khiếu nại mất công quá · Nghĩ khiếu nại cũng không được gì · Không bực đến mức đó · Khác (không bắt buộc)

**Phần 4 — Kể lại**
11. Kể ngắn lần gần nhất đơn đồ ăn của bạn có vấn đề (trễ, thiếu món…): chuyện gì xảy ra, bạn làm gì, khó chịu nhất ở đâu? (không bắt buộc)

## Mỗi câu dùng cho phần nào

- Câu 3 × câu 4 → số lần giao trễ / người / tháng: impact (`spec.md` §2) và persona chi phí (`cost/personas.yaml`).
- Câu 4 so với câu 5 → giao trễ hay thiếu món phổ biến hơn: nguồn thứ hai kiểm lại kết quả review (`evidence/data-mining.md`).
- Câu 7–10 → pain nằm ở đâu và mỗi lần mất bao lâu.
- Câu 11 → trích dẫn nguyên văn và ý cho câu thử.
