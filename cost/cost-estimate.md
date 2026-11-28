# Chi phí khi dùng thật

> Số lấy từ `cost/simulate-1-summary.md` (do `python run.py simulate` sinh ra), không điền tay.
> Lúc build dùng tài khoản trả phí OpenAI; giá tính theo bảng giá công khai.

## 1. Đầu vào

- **Persona** (`cost/personas.yaml`), từ khảo sát 21 người có đặt đơn (câu 3 × câu 4, `evidence/survey/count_survey.py`):
  - `dat_it` 43% (9/21) · ~1,7 phiên / tháng · 1 lượt / phiên
  - `dat_vua` 33% (7/21) · ~4,4 phiên / tháng · 1 lượt / phiên
  - `dat_nhieu` 24% (5/21) · ~11 phiên / tháng · 2 lượt / phiên *(lượt / phiên: tự ước tính)*
  - Giả định mỗi đơn trễ khách mở trợ lý 1 lần — **mức trần** *(tự ước tính)*; hiện chỉ 4/16 người từng khiếu nại trong app.
- **Số người dùng thật** 3 kịch bản: thấp 910 (hơn 1.000 học viên AI20K × 21/23 có đặt đơn, nguồn: `01-challenge-brief.md` + khảo sát) · cơ sở 10.000 · cao 100.000 *(tự ước tính — chưa có nguồn công khai về số người dùng app giao đồ ăn)*
- **Giá** 3 mức model (bảng giá bộ đề `further-reading/model-prices.csv`, https://developers.openai.com/api/docs/pricing, xem 25/11/2026): `gpt-5-nano` $0,05 / $0,40 · `gpt-5-mini` $0,25 / $2,00 · `gpt-6.1-terra` $1,00 / $5,00 (USD / 1 triệu token vào / ra)
- **Tỉ lệ đạt** dùng để tính: 20/20 (100%) — lượt `run-3` (cùng cấu hình code với bản chạy mô phỏng; lượt `run-2` cũng 20/20 nhưng câu trả lời là câu mẫu do lỗi bước kiểm, xem `eval/report.md` §3)
- Đo token trên model `gpt-5-nano`, tính giá `gpt-5-nano`, `gpt-5-mini`, `gpt-6.1-terra` (cùng hãng, cùng bộ tách token — sai lệch nhỏ)

## 2. Kết quả mô phỏng

Lượt mô phỏng: `cost/simulate-1.csv` · run ID `simulate-1@20261128-092440` · 50 phiên · seed 42 · 0 phiên lỗi

| Persona | Số phiên | Lượt / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên |
|---|---:|---:|---:|---:|---:|
| dat_it | 21 | 1 | 569 | 1.718 | 1,7 |
| dat_vua | 21 | 1 | 628 | 1.701 | 1,9 |
| dat_nhieu | 8 | 2 | 1.022 | 3.099 | 3,1 |

| Model | Chi phí / phiên | Chi phí / task thành công | / tháng — thấp (910) | / tháng — cơ sở (10.000) | / tháng — cao (100.000) | / người / tháng (cơ sở) |
|---|---|---|---|---|---|---|
| gpt-5-nano | $0,00081 (≈ 21 ₫) | $0,00081 (≈ 21 ₫) | $4,52 (≈ 117 nghìn ₫) | $49,64 (≈ 1,29 triệu ₫) | $496,38 (≈ 12,9 triệu ₫) | $0,0050 (≈ 129 ₫) |
| gpt-5-mini | $0,0040 (≈ 105 ₫) | $0,0040 (≈ 105 ₫) | $22,59 (≈ 587 nghìn ₫) | $248,19 (≈ 6,45 triệu ₫) | $2.481,90 (≈ 64,5 triệu ₫) | $0,0248 (≈ 645 ₫) |
| gpt-6.1-terra | $0,0103 (≈ 268 ₫) | $0,0103 (≈ 268 ₫) | $57,84 (≈ 1,5 triệu ₫) | $635,57 (≈ 16,5 triệu ₫) | $6.355,67 (≈ 165 triệu ₫) | $0,0636 (≈ 1.652 ₫) |

Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt (100% → bằng chi phí / phiên). Tỉ giá 26.000 ₫ / USD *(tự ước tính)*.
Token ra lớn gấp ~3 token vào vì `gpt-5-nano` tính cả token suy luận.

## 3. So với impact

- Impact / người / tháng (`spec.md` §2): ~5,1 đơn trễ × ~32 phút ≈ **163 phút chờ / người / tháng**, và ~13/16 lần trễ không được bù gì.
- Chi phí model / người / tháng (cơ sở, `gpt-5-nano`): **≈ 129 ₫** ($0,005); kể cả model mạnh nhất trong bảng chỉ ≈ 1.652 ₫.
- **Kết luận một dòng — đáng làm không:** chi phí **model** gần như không đáng kể so với thiệt hại của người dùng → **đáng làm (go)** với `gpt-5-nano`; chi phí thật nằm ở **voucher phát ra và giờ công nhân viên duyệt** (mục 4), không phải ở model.

## 4. Chi phí ngoài model *(tự ước tính, chưa đo)*

- **Voucher phát ra:** mỗi phiên đủ điều kiện được đề xuất 15.000–50.000 ₫ — lớn gấp hàng nghìn lần chi phí model. Đây là chi phí kinh doanh của chính sách, sản phẩm giúp phát **đúng mức** (không vượt hạn mức, 20/20 câu ở `dung_so_lieu`, `khong_vuot_han_muc`).
- **Giờ công duyệt bản nháp:** nếu mỗi bản nháp mất ~30 giây duyệt *(tự ước tính)*, kịch bản cơ sở ≈ 10.000 × (0,43×1,7 + 0,33×4,4 + 0,24×11) ≈ 48.000 phiên / tháng → tối đa ~400 giờ công / tháng (chỉ phần đề xuất voucher cần duyệt). Cách giảm: cho tự phát voucher nhỏ nhất (15.000 ₫) khi khách lần đầu khiếu nại — cần đổi mức tự động ở `spec.md` §4.
- Hosting, lưu trữ: không tính (bản chạy thử chạy cục bộ).
