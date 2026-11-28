# Reflection — Lê Minh Phụng

1. **Vai trò + phần mình làm (trỏ tới file / commit):**
   Mình phụ trách bằng chứng pain qua khảo sát (`evidence/survey/`) và phần tổng hợp bằng chứng (`evidence/summary.md`). Khảo sát Google Form 11 câu, hỏi theo "5 đơn gần nhất", thu 23 phiếu, 21 người có đặt đồ ăn qua app: 14/19 người gặp ít nhất 1 đơn giao trễ trong 5 đơn gần nhất, 13/16 lần trễ gần nhất không được bù gì hoặc không khiếu nại; lý do không khiếu nại hay gặp nhất là "nghĩ khiếu nại cũng không được gì" (5) và "mất công quá" (4). Mình trình bày trang 1 (người dùng & pain) và trang 7 (kết luận).

2. **AI hỗ trợ mình thế nào (việc gì, công cụ gì, chỗ nào phải sửa lại output AI):**
   Nhóm dùng Claude Code để soạn bộ câu hỏi, viết script Apps Script tạo form (`create_form.gs`) và script đếm (`count_survey.py`), và soạn nháp `evidence/summary.md`. Câu trả lời khảo sát là của người thật, AI không viết thay. Chỗ phải chỉnh: câu hỏi ban đầu hỏi "trong 1 tháng qua" khó nhớ, nhóm đổi sang "trong 5 đơn gần nhất"; con số "~5,1 đơn trễ / người / tháng" và "~32 phút" là quy đổi theo điểm giữa các khoảng lựa chọn, phải ghi rõ *(tự ước tính)* để không trình bày như số đo chính xác.

3. **Một câu thử trượt của nhóm và mình học được gì:**
   T07 ở lượt 1: đơn trễ 19 phút (chưa tới ngưỡng 20) nhưng trợ lý vẫn nói "voucher là đề xuất, nhân viên sẽ duyệt", khiến khách tưởng mình có voucher. Câu này chạm đúng pain khảo sát cho thấy: khách "không biết có được bù gì" — trả lời mập mờ còn tệ hơn không trả lời. Mình học được: bằng chứng pain không chỉ để mở đầu slide mà phải dùng để chọn tiêu chí chấm (nói rõ được bù gì, vì sao). Ngoài ra, khảo sát cho thấy thiếu món cũng phổ biến (13/20) dù review gần như không nhắc — hai nguồn lệch nhau thì phải giải thích, không bỏ qua.
