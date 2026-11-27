"""Đếm kết quả khảo sát: python evidence/survey/count_survey.py

Đọc evidence/survey/results.csv (bản đã xoá cột Dấu thời gian). Cột theo thứ tự câu 1..11 trong questions.md.
Quy đổi dùng cho impact (tự ước tính, ghi rõ trong spec §2):
  - câu 3 (đơn / tuần) lấy điểm giữa: 1–2 → 1.5 · 3–5 → 4 · 6–10 → 8 · Trên 10 → 12
  - câu 6 (phút trễ) lấy điểm giữa: 15–30 → 22.5 · 30–60 → 45 · Trên 60 → 75
  - 1 tháng = 4.3 tuần
"""
import csv
from collections import Counter
from pathlib import Path

PATH = Path(__file__).with_name("results.csv")
ORDERS_PER_WEEK = {"1–2": 1.5, "3–5": 4, "6–10": 8, "Trên 10": 12}
DELAY_MIN = {"15–30 phút": 22.5, "30–60 phút": 45, "Trên 60 phút": 75}
WEEKS_PER_MONTH = 4.3

with open(PATH, encoding="utf-8-sig") as f:
    rows = list(csv.reader(f))[1:]
Q = lambda r, i: r[i - 1].strip()          # câu i → cột i-1

print(f"Tổng phiếu: {len(rows)}")
users = [r for r in rows if Q(r, 3) in ORDERS_PER_WEEK]
print(f"Có đặt đơn qua app (câu 3 ≠ 0, không kết thúc sớm): {len(users)}/{len(rows)}")
print("Câu 1:", dict(Counter(Q(r, 1) for r in users)))
print("Câu 2:", dict(Counter(Q(r, 2) for r in users)))
print("Câu 3:", dict(Counter(Q(r, 3) for r in users)))

for q, name in ((4, "GIAO TRỄ"), (5, "THIẾU / SAI MÓN")):
    known = [int(Q(r, q)) for r in users if Q(r, q).isdigit()]
    hit = sum(1 for x in known if x > 0)
    print(f"\nCâu {q} ({name}) — ≥1 đơn trong 5 đơn gần nhất: {hit}/{len(known)} ({hit / len(known):.0%})"
          f" · không nhớ: {len(users) - len(known)}")
    print(f"  theo đơn: {sum(known)}/{5 * len(known)} đơn ({sum(known) / (5 * len(known)):.0%})")

late = [r for r in users if Q(r, 6)]       # người đã trả lời phần "lần giao trễ gần nhất"
print(f"\nPhần 3 (lần giao trễ gần nhất): {len(late)} người")
for q in (6, 8, 9, 10):
    print(f"Câu {q}:", dict(Counter(Q(r, q) or "(bỏ trống)" for r in late)))
print("Câu 7:", dict(Counter(x for r in late for x in Q(r, 7).split(";") if x)))
no_gain = sum(1 for r in late if Q(r, 8) in ("Không được gì", "Không khiếu nại nên không biết"))
print(f"Lần trễ gần nhất không được bù gì / không khiếu nại: {no_gain}/{len(late)}")

# Impact: số đơn trễ / người / tháng và phút trễ / lần
per_user = [ORDERS_PER_WEEK[Q(r, 3)] * WEEKS_PER_MONTH * int(Q(r, 4)) / 5
            for r in users if Q(r, 4).isdigit()]
mins = [DELAY_MIN[Q(r, 6)] for r in late if Q(r, 6) in DELAY_MIN]
print(f"\nĐơn trễ / người / tháng (trung bình, {len(per_user)} người): {sum(per_user) / len(per_user):.1f}")
print(f"Phút trễ / lần (trung bình, {len(mins)} người nhớ): {sum(mins) / len(mins):.0f}")
for band in ORDERS_PER_WEEK:
    g = [ORDERS_PER_WEEK[Q(r, 3)] * WEEKS_PER_MONTH * int(Q(r, 4)) / 5
         for r in users if Q(r, 3) == band and Q(r, 4).isdigit()]
    if g:
        print(f"  nhóm {band} đơn/tuần: {len(g)} người · {sum(g) / len(g):.1f} đơn trễ / tháng")
