# Tổng hợp bằng chứng pain

> Điền ở guide bước 1.2, xong trước **CP3 10:00 Thứ Bảy 28/11**. Chấm ở rubric R1.
> Ba nguồn ngang nhau — tối thiểu **≥1 nguồn đạt ngưỡng**. Mạnh nhất: đào data ra insight → hỏi người dùng để kiểm lại (hoặc ngược lại).

## 1. Nguồn đã dùng

| Nguồn | Đạt ngưỡng? | File |
|---|---|---|
| Đào data (x/N, %, cách đếm chạy lại được, ≥5 ví dụ) | ☑ — 150 review ShopeeFood Google Play, đếm bằng script | `evidence/data-mining.md` · `evidence/reviews-shopeefood.csv` · `evidence/count_reviews.py` |
| Phỏng vấn (≥3 người ngoài nhóm, đúng người dùng) | ☐ — chưa làm | `evidence/interviews/` |
| Khảo sát (≥20 người ngoài nhóm, đúng người dùng) | ☑ — 23 phiếu, 21 người có đặt đồ ăn qua app | `evidence/survey/questions.md` · `evidence/survey/results.csv` · `evidence/survey/count_survey.py` |

## 2. Số chính

- Đào data (150 review mới nhất ShopeeFood, 11–26/11/2026): **giao trễ 13/150 (8,7%) · 12/50 (24%) review 1–3 sao** · thiếu món 0/150 · sai món 1/150 · khiếu nại khó / hoàn tiền chậm 3/150.
- Khảo sát: n = 23 phiếu, **21 người có đặt đồ ăn qua app** (13 sinh viên · 5 đi làm · 3 khác; 12 dùng ShopeeFood, 6 GrabFood):
  - **≥1 đơn giao trễ trong 5 đơn gần nhất: 14/19 (74%)** (2 người không nhớ) · theo đơn: 24/95 đơn (25%)
  - ≥1 đơn thiếu / sai món trong 5 đơn gần nhất: 13/20 (65%) (1 người không nhớ) · theo đơn: 24/100 đơn (24%)
  - Lần giao trễ gần nhất (16 người): **13/16 không được bù gì hoặc không khiếu nại** · chỉ 4/16 khiếu nại trong app · 8/16 "bỏ qua, chờ tiếp"
  - Vì sao không khiếu nại: "nghĩ khiếu nại cũng không được gì" 5 · "khiếu nại mất công quá" 4 · "không bực đến mức đó" 3 (4 bỏ trống)
  - Trễ bao lâu (13 người nhớ): 15–30 phút 9 · 30–60 phút 3 · trên 60 phút 1 → trung bình ~32 phút *(quy đổi điểm giữa, xem `count_survey.py`)*
  - Ước tính **~5,1 đơn trễ / người / tháng** (câu 3 × câu 4, quy đổi điểm giữa, 1 tháng = 4,3 tuần) — nhóm 1–2 đơn/tuần: 1,7 · 3–5 đơn/tuần: 4,4 · trên 10 đơn/tuần: 10,3

Chạy lại: `python evidence/count_reviews.py` · `python evidence/survey/count_survey.py`

## 3. ≥5 trích dẫn hoặc ví dụ nguyên văn (có nguồn, bỏ tên)

1. "Đặt mỳ idomie từ 7r app báo 8h30 nma ship đến 9r mới gọi nhận đồ" — phiếu khảo sát #2
2. "Đặt gà mất 1 tiếng hơn vì ko có shipper nhận đơn" — phiếu khảo sát #3
3. "đơn đến trễ, nhưng tôi chẳng làm gì cả" — phiếu khảo sát #1
4. "Khó chịu nhất là app không cập nhật giờ giao, còn khiếu nại thì thấy mất công nên thôi." — phiếu khảo sát #17
5. "voucher thì không bù được thời gian" — phiếu khảo sát #18
6. "ghép đơn giao trễ hẳn 1 tiếng" — review #26 (1★, `evidence/reviews-shopeefood.csv`)
7. "đặt từ 10h37 mà 12h07 mới nhận đồ ăn" — review #53 (1★)

(Số phiếu = thứ tự dòng trong `evidence/survey/results.csv`.)

## 4. Các nguồn có khớp nhau không

Review nói: trong các vấn đề về một đơn, **giao trễ** nổi bật nhất (24% review 1–3 sao), thiếu / sai món gần như không có (1/150). Khảo sát nói: **giao trễ phổ biến** (74% người gặp trong 5 đơn gần nhất) — **khớp**; nhưng thiếu / sai món **cũng phổ biến gần ngang** (65%) — **lệch** với review.
Giải thích chỗ lệch: review Play Store chủ yếu chấm **app** (lag, lỗi, phí), và người bị thiếu món thường xử lý với quán / shipper chứ không viết review; khảo sát hỏi thẳng từng đơn nên bắt được cả thiếu món. Hai nguồn **khớp ở điểm chính của lát cắt**: giao trễ hay gặp và người dùng **hiếm khi được bù / bỏ qua không khiếu nại** (13/16 khảo sát; review #15, #116 về khiếu nại không được giải quyết).
Giới hạn: mẫu khảo sát nhỏ, chủ yếu học viên trẻ quen app, gửi qua kênh của nhóm; "5 đơn gần nhất" là trí nhớ, có thể lệch.

## 5. Kết luận

Giả thuyết ở `evidence/hypothesis.md`: **phải đổi** — giả thuyết về thiếu / sai món: phần khảo sát đạt (13/20 ≥ 30%, nhưng đo theo "5 đơn gần nhất" chứ không phải "1 tháng qua"), phần review **không đạt** (4/50 review 1–3 sao < 15%), và khảo sát không hỏi hành vi khiếu nại riêng cho thiếu món. Giao trễ có bằng chứng ở **cả hai nguồn** và có bằng chứng về chỗ vướng (không biết được bù gì, ngại khiếu nại) → nhóm chọn lát cắt **khiếu nại giao trễ**.
Điều vẫn chưa biết: khách có thật sự khiếu nại nhiều hơn nếu biết ngay mức bù không; chính sách bù trễ thật của các app (đang dùng bảng tự đặt); người bị trễ có chấp nhận voucher thay cho thời gian mất không (phiếu #18).

## Lịch hẹn (dùng cho CP2 — chỉ ghi vai và giờ, không tên)

| Vai | Giờ hẹn | Đã xong? |
|---|---|---|
| Người đặt đồ ăn (khảo sát online) | 27/11 18:07 → 19:10 | Xong — 23 phiếu |
