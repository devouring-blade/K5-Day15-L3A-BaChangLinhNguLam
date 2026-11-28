# Khai báo dùng AI

README của nhóm có mục "Dùng AI vào việc gì" (2–3 dòng, bắt buộc). Ghi chi tiết vào bảng dưới đây.

> Luật của đề: dùng AI để làm bài thoải mái, nhưng **ai không giải thích được phần có tên mình thì phần đó nhận 0 điểm**. Khai thiếu không bị trừ; giấu mới bị.

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
|---|---|---|---|---|
| Code bản chạy thử | Claude Code (Claude) | Viết `codebase/agent.py`, `tools.py`, phần gọi OpenAI trong `ai.py` theo sơ đồ `spec.md` §4 | Chạy thử 20 câu ở chế độ giả; người phụ trách đọc hiểu từng hàm: __ | Nguyễn Sỹ Huy Kiên |
| Prompt / thiết kế lời gọi mô hình | Claude Code (Claude) | Viết 2 prompt (`SYSTEM_PARSE`, `SYSTEM_REPLY`) và bước code kiểm số tiền sau AI | __ | Nguyễn Sỹ Huy Kiên |
| Đào data (viết script đếm, gợi ý nhãn) | Claude Code (Claude) | Thu 150 review công khai ShopeeFood trên Google Play (không lấy tên), gắn nhãn nháp theo định nghĩa trong `evidence/data-mining.md`, viết `evidence/count_reviews.py` | Kiểm tay __ dòng, khớp __ | Đào Trường Vũ |
| Rà câu hỏi phỏng vấn / khảo sát | Claude Code (Claude) | Soạn bộ 11 câu và viết script Apps Script `evidence/survey/create_form.gs` tạo Google Form; viết `count_survey.py` | Nhóm duyệt câu hỏi, tự gửi form, câu trả lời là của người thật | Lê Minh Phụng |
| Viết câu thử (benchmark) | Claude Code (Claude) | Viết 20 câu thử, 5 metric; 9 câu viết lại từ phiếu khảo sát / review thật (cột `source`), 11 câu tự viết theo `spec.md` §5 | Nhóm duyệt chuẩn "đạt" trước 19:30 27/11; kiểm đáp án với data: __ | Vũ Lê Hoàng |
| Sinh data `synthetic` (nếu có) | Claude Code (Claude) | Viết tay 12 đơn giả, bảng chính sách tự đặt, lịch sử khiếu nại (không dùng seed) | Kiểm tay __/12 đơn | Vũ Lê Hoàng |
| Chấm cột `pass` bằng LLM (nếu có) | Claude Code (Claude) — nếu dùng | Chấm nháp cột `pass` theo `eval/metric_spec.yaml` | Người chấm lại độc lập __ câu, khớp __/__ | __ |
| Slide, văn bản | Claude Code (Claude) | Soạn nháp `spec.md`, `canvas.md`, `evidence/summary.md`, `data/DATA_CARD.md`, `README.md` | Nhóm đọc lại, sửa: __ | Cả nhóm |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).
