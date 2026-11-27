# Đào data — cách đếm và kết quả

> Điền ở guide bước 1.2. Ôn lại: ngày 2, ngày 6 · lab ngày 2, lab ngày 6.
> Script / công thức đếm để trong repo, người khác chạy lại phải ra cùng số.

## 1. Cách đếm — viết TRƯỚC khi chạy

- Data dùng: review công khai của app **ShopeeFood** (`com.deliverynow`) trên Google Play, trang tiếng Việt (`hl=vi&gl=VN`), xem ngày **27/11/2026**. Link: https://play.google.com/store/apps/details?id=com.deliverynow&hl=vi&gl=VN
- Chọn mẫu: **150 review mới nhất** (sắp theo "Mới nhất", **mọi mức sao**, mọi thiết bị mặc định "Điện thoại"), trải từ 11/11/2026 đến 26/11/2026. Không lọc theo nội dung.
- Đếm gì: số review thuộc từng nhãn bên dưới · trên tập: 150 review · lọc gì: không lọc (có đếm thêm riêng nhóm 1–3 sao, ghi rõ)
- **Mẫu số:** 150 (mọi review đã đọc, kể cả không liên quan). Phần riêng 1–3 sao: mẫu số 50.
- Nhãn (mỗi review một nhãn chính, nhãn phụ ghi ở `ghi_chu`):
  - `thieu_mon` — nói nhận đơn thiếu món / quên món
  - `sai_mon` — nói giao nhầm món / món không đúng đã đặt
  - `giao_tre` — nói giao lâu, trễ so với dự kiến, chờ tài xế nhận đơn lâu, hoặc phàn nàn ghép đơn (nguyên nhân giao lâu)
  - `khieu_nai_hoan_tien` — nói khó khiếu nại, CSKH không giải quyết, hoàn tiền chậm / không hoàn
  - `van_de_don_khac` — vấn đề khác về một đơn cụ thể (không hủy được đơn, đơn bị hủy…)
  - `khac` — vấn đề app, phí, voucher, thanh toán, địa chỉ, hoặc chê chung chung không rõ vấn đề
  - `khong_lien_quan` — khen / không có nội dung phàn nàn
  - Review mơ hồ (vd "Quá lâu" không rõ app chậm hay giao chậm) → `khac`, ghi lý do ở `ghi_chu`.
- Script: `python evidence/count_reviews.py` (đọc `evidence/reviews-shopeefood.csv`)

## 2. Đọc trước, đếm sau

Đã đọc cả 150 review trước khi chốt nhãn. Các *kiểu* thấy được: khen ngắn ("ok", "tốt"); giao lâu do ghép đơn / chờ tài xế; lỗi app (lag, định vị, thanh toán, OTP); phí và voucher; không hủy được đơn; CSKH không giải quyết, hoàn tiền chậm; rất ít review nói thiếu / sai món.

## 3. Kết quả

| Đếm gì | x / N | % | Ghi chú |
|---|---|---|---|
| `thieu_mon` | 0/150 | 0% | không review nào trong mẫu |
| `sai_mon` | 1/150 | 0,7% | |
| `khieu_nai_hoan_tien` | 3/150 | 2,0% | |
| `giao_tre` | 13/150 | 8,7% | **vấn đề về đơn hay gặp nhất** |
| `van_de_don_khac` | 2/150 | 1,3% | |
| `khac` | 36/150 | 24,0% | chủ yếu lỗi app, phí |
| `khong_lien_quan` | 95/150 | 63,3% | |
| Riêng 1–3 sao: `giao_tre` | 12/50 | 24% | |
| Riêng 1–3 sao: thiếu/sai món + khiếu nại hoàn tiền | 4/50 | 8% | ngưỡng giả thuyết là ≥15% → **không đạt** |

**Kết luận so với `evidence/hypothesis.md`:** phần review của giả thuyết **không đạt** (8% < 15% trên review 1–3 sao). Trong mẫu này, thiếu / sai món hiếm được nhắc; vấn đề về đơn nổi bật nhất là **giao trễ** (24% review 1–3 sao), thường kèm ghép đơn.

## 4. ≥5 ví dụ cụ thể (số thứ tự dòng trong `reviews-shopeefood.csv`, đã bỏ tên người viết)

1. #26 (1★, giao_tre): "ghép đơn giao trễ hẳn 1 tiếng"
2. #53 (1★, giao_tre): "đặt từ 10h37 mà 12h07 mới nhận đồ ăn"
3. #129 (2★, giao_tre): "tận 1 tiếng mới nhận dc đồ ăn nguội hết luôn"
4. #15 (1★, khieu_nai_hoan_tien): đơn bị hủy, "2 tháng trời … ko hoàn lại tiền"
5. #116 (1★, khieu_nai_hoan_tien): "Nhân viên shoppee k hiểu câu hỏi, k giải quyết được vấn đề của tôi"
6. #51 (1★, sai_mon): "shop không có hàng vẫn giao loại ko đúng"

## 5. Giới hạn của data

- Một app, một nền tảng (Google Play), 150 review trong ~2 tuần. Review Play Store hay nói về **app** (lag, lỗi) hơn là về **một đơn**; người viết thường đang bực, nên % trong review không phải % mọi người dùng.
- Người thiếu món có thể khiếu nại trong app mà không viết review → review có thể đánh giá thấp tần suất thiếu món.
- Nhãn gắn theo định nghĩa ở mục 1; người thứ hai đọc lại độc lập ít nhất 30 dòng để kiểm độ khớp: __/30.
- → Kiểm lại bằng: khảo sát ≥20 người ngoài nhóm (hỏi số lần thiếu / sai món **và** giao trễ trong 1 tháng qua).
