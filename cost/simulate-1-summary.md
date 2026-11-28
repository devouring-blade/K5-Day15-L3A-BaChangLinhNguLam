# Tóm tắt mô phỏng simulate-1@20261128-092440

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| dat_it | 21 | 1 | 569 | 1718 | 1.7 | 3.9 |
| dat_vua | 21 | 1 | 628 | 1701 | 1.9 | 4.5 |
| dat_nhieu | 8 | 2 | 1022 | 3099 | 3.1 | 7.2 |

Tỉ lệ đạt dùng để tính: 20/20 (100%) — lượt run-3@20261128-091039

- Tỉ lệ đạt lấy từ lượt nhóm chọn: eval/run-3.csv (--rate-from).

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (910 người) | Chi phí / tháng — cơ sở (10.000 người) | Chi phí / tháng — cao (100.000 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gpt-5-nano (vào 0.05 · ra 0.4 $/1M) | $0.00081 (≈ 21 ₫) | $0.00081 (≈ 21 ₫) | $0.00069 (≈ 18 ₫) | $4.52 (≈ 117.443 ₫) | $49.64 (≈ 1.290.587 ₫) | $496.38 (≈ 12.905.868 ₫) | $0.0050 (≈ 129 ₫) |
| gpt-5-mini (vào 0.25 · ra 2.0 $/1M) | $0.0040 (≈ 105 ₫) | $0.0040 (≈ 105 ₫) | $0.0035 (≈ 90 ₫) | $22.59 (≈ 587.217 ₫) | $248.19 (≈ 6.452.934 ₫) | $2,481.90 (≈ 64.529.341 ₫) | $0.0248 (≈ 645 ₫) |
| gpt-6.1-terra (vào 1.0 · ra 5.0 $/1M) | $0.0103 (≈ 268 ₫) | $0.0103 (≈ 268 ₫) | $0.0089 (≈ 231 ₫) | $57.84 (≈ 1.503.752 ₫) | $635.57 (≈ 16.524.748 ₫) | $6,355.67 (≈ 165.247.479 ₫) | $0.0636 (≈ 1.652 ₫) |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (1.2) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: gpt-5-nano. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 0/50.
- Tỷ giá: 1 USD = 26.000 ₫ ((tự ước tính) tỉ giá tham khảo tháng 11/2026).
