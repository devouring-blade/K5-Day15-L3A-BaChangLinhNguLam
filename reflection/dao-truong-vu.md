# Reflection — Đào Trường Vũ

1. **Vai trò + phần mình làm (trỏ tới file / commit):**
   Mình phụ trách đào review công khai và mô phỏng chi phí. Review: 150 review mới nhất của ShopeeFood trên Google Play, mọi mức sao (`evidence/reviews-shopeefood.csv`, `evidence/data-mining.md`, script `evidence/count_reviews.py`) — giao trễ 12/50 review 1–3 sao, thiếu món 0/150; kết quả này làm nhóm đổi lát cắt từ thiếu món sang giao trễ. Chi phí: `cost/personas.yaml` (3 persona từ khảo sát: đặt ít 43% · vừa 33% · nhiều 24%), `cost/cost-estimate.md` — gpt-5-nano ≈ 21 ₫ / task thành công, ≈ 1,29 triệu ₫ / tháng ở 10.000 người. Mình trình bày trang 2 (vì sao chọn bài này) và trang 6 (chi phí khi dùng thật).

2. **AI hỗ trợ mình thế nào (việc gì, công cụ gì, chỗ nào phải sửa lại output AI):**
   Nhóm dùng Claude Code để thu 150 review (không lấy tên người viết), gắn nhãn nháp theo định nghĩa viết trước, viết script đếm, điền persona và chạy `python run.py simulate` 50 phiên. Nhãn được người thứ hai trong nhóm gắn lại 30 dòng, khớp 30/30. Chỗ phải cẩn thận: quy mô 10.000 / 100.000 người không có nguồn công khai nên ghi *(tự ước tính)*; giả định "mỗi đơn trễ mở trợ lý 1 lần" là mức trần vì thực tế chỉ 4/16 người từng khiếu nại; mẫu số đếm review là cả 150 review, kể cả review không liên quan.

3. **Một câu thử trượt của nhóm và mình học được gì:**
   T16 ở lượt 1: khách báo "vừa trễ vừa thiếu ly trà sữa" — trợ lý đề xuất đúng 30.000đ nhưng ghi lý do "do thiếu món", trong khi tiền là để bù phần trễ 45 phút. Mình học được: một tin của khách thường có nhiều vấn đề (đúng như review thật hay kể lẫn trễ + thiếu món), nên phải tách phần trong phạm vi và phần chuyển người. Về chi phí: tiền model chỉ ≈ 129 ₫ / người / tháng, cái đắt thật là voucher phát ra và giờ công nhân viên duyệt — con số này đổi cách nhóm trả lời câu "có đáng làm không".
