"""Đếm nhãn review: python evidence/count_reviews.py [file.csv]

Mặc định đọc evidence/reviews-shopeefood.csv. Mẫu số = mọi review đã gắn nhãn (kể cả không liên quan).
"""
import csv
import sys
from collections import Counter
from pathlib import Path

path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("reviews-shopeefood.csv")
with open(path, encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

n = len(rows)
by_label = Counter(r["nhan"] for r in rows)
print(f"{path.name}: N = {n} review")
for label, x in by_label.most_common():
    print(f"  {label:22s} {x:4d}/{n}  ({x / n:.1%})")

low = [r for r in rows if r["so_sao"] in ("1", "2", "3")]
print(f"\nRiêng review 1-3 sao: N = {len(low)}")
for label, x in Counter(r["nhan"] for r in low).most_common():
    print(f"  {label:22s} {x:4d}/{len(low)}  ({x / len(low):.1%})")

group = {"thieu_mon", "sai_mon", "khieu_nai_hoan_tien"}
x = sum(by_label[g] for g in group)
print(f"\nNhóm giả thuyết (thieu_mon + sai_mon + khieu_nai_hoan_tien): {x}/{n} ({x / n:.1%})")
xl = sum(1 for r in low if r["nhan"] in group)
print(f"  trên review 1-3 sao: {xl}/{len(low)} ({xl / len(low):.1%})")
