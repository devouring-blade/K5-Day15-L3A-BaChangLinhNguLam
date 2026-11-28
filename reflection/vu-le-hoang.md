# Reflection — Vũ Lê Hoàng

1. **Vai trò + phần mình làm (trỏ tới file / commit):**
   Mình phụ trách data chạy thử và bộ câu thử: `data/don_hang.csv` (12 đơn phủ các ca trễ 12 → 75 phút, giao sớm, đơn huỷ, đơn 300.000đ), `data/chinh_sach.csv` (bậc bù tự đặt: trễ ≥20' → 15.000đ, ≥40' → 30.000đ, ≥60' → 50.000đ), `data/lich_su_khieu_nai.csv`, `data/DATA_CARD.md`, `eval/benchmark.csv` (20 câu: thường 5 · khó 12 · từ chối 3, trong đó 9 câu từ lời khách / review thật) và `eval/metric_spec.yaml` (5 metric). Mình trình bày trang 5 (đánh giá thế nào) và trang 8 (nếu có thêm 1 tuần), và đọc câu thử trong phần demo.

2. **AI hỗ trợ mình thế nào (việc gì, công cụ gì, chỗ nào phải sửa lại output AI):**
   Nhóm dùng Claude Code để viết nháp data giả, câu thử và metric theo kịch bản ở `spec.md` §5. Chỗ phải giữ chặt: mỗi câu thử có cột `source` ghi đúng nguồn (số phiếu khảo sát / số review), không câu nào tự nhận là lời người dùng nếu do nhóm tự viết; chính sách bù ghi rõ là tự đặt, vì trang trợ giúp Shopee ("Giao nhanh đúng hẹn") nói không áp dụng cho ShopeeFood và không công bố giá trị voucher. Sau 19:30 thứ Sáu, chuẩn "đạt", metric và cột `expected` giữ nguyên, không sửa cho khớp output.

3. **Một câu thử trượt của nhóm và mình học được gì:**
   T04 ở lượt 1: đơn trễ 59 phút — trợ lý đưa đúng 30.000đ nhưng không nói "59 phút", nên khách không hiểu vì sao không phải mức 50.000đ (≥60 phút). Câu này được đặt cố ý sát ngưỡng. Mình học được: câu thử "sát ngưỡng" bắt được lỗi mà câu thường không bắt được, và `pass_criterion` phải ghi rõ dữ kiện bắt buộc (số phút) chứ không chỉ "đúng số tiền". Lượt 3 đạt 20/20, nhưng bộ 20 câu nhóm đã biết trước — muốn tin hơn thì cần thêm câu thử lạ.
