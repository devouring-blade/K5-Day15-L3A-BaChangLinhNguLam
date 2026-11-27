"""Công cụ của bài toán: khiếu nại đơn đồ ăn giao trễ (khớp bảng công cụ ở spec.md §4).

Dữ liệu đọc từ data/ (mô tả ở data/DATA_CARD.md, nhãn synthetic).
Công cụ có tác động ra ngoài (draft_voucher, escalate_to_human) KHÔNG tự làm gì thật:
chỉ trả bản nháp / ca chờ để nhân viên duyệt.
"""
import csv
import os
from datetime import datetime

from tracing import tool, TOOLS  # noqa: F401

DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
TIME_FMT = "%Y-%m-%d %H:%M"


def _read(name):
    with open(os.path.join(DATA, name), encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


@tool
def get_order(ma_don: str) -> dict:
    """get_order · input: mã đơn (str) · output: dict đơn (giờ đặt, giờ giao dự kiến, giờ giao thực tế,
    tổng tiền, trạng thái, mã khách) hoặc {"found": False} · không tác động ra ngoài (chỉ đọc)."""
    for row in _read("don_hang.csv"):
        if row["ma_don"].upper() == (ma_don or "").strip().upper():
            return dict(row, found=True)
    return {"found": False, "ma_don": ma_don}


@tool
def get_policy(loai_su_co: str = "giao_tre") -> dict:
    """get_policy · input: loại sự cố (str, hiện chỉ "giao_tre") · output: {"bac": [(từ phút, đến phút, mức bù)],
    "han_muc": số tiền} · không tác động ra ngoài (chỉ đọc)."""
    rows = _read("chinh_sach.csv")
    bac = [(int(r["tre_tu_phut"]), int(r["tre_den_phut"]), int(r["muc_bu"]))
           for r in rows if r["loai_su_co"] == loai_su_co]
    han_muc = next(int(r["muc_bu"]) for r in rows if r["loai_su_co"] == "han_muc")
    return {"loai_su_co": loai_su_co, "bac": bac, "han_muc": han_muc}


@tool
def get_complaint_history(ma_khach: str) -> dict:
    """get_complaint_history · input: mã khách (str) · output: {"so_lan_30_ngay": int} · không tác động ra ngoài."""
    for row in _read("lich_su_khieu_nai.csv"):
        if row["ma_khach"] == ma_khach:
            return {"ma_khach": ma_khach, "so_lan_30_ngay": int(row["so_lan_khieu_nai_tre_30_ngay"])}
    return {"ma_khach": ma_khach, "so_lan_30_ngay": 0}


@tool
def compute_delay_compensation(order: dict, policy: dict) -> dict:
    """compute_delay_compensation · input: đơn (dict từ get_order), chính sách (dict từ get_policy)
    · output: {"phut_tre": int | None, "muc_bu": int, "nguong": int, "ly_do": str} — TÍNH BẰNG CODE, không phải AI
    · không tác động ra ngoài."""
    if not order.get("gio_giao_thuc_te"):
        return {"phut_tre": None, "muc_bu": 0, "nguong": policy["bac"][1][0], "ly_do": "đơn chưa giao / không có giờ giao"}
    du_kien = datetime.strptime(order["gio_giao_du_kien"], TIME_FMT)
    thuc_te = datetime.strptime(order["gio_giao_thuc_te"], TIME_FMT)
    phut = int((thuc_te - du_kien).total_seconds() // 60)
    muc = 0
    for tu, den, bu in policy["bac"]:
        if tu <= phut <= den:
            muc = bu
    muc = min(muc, policy["han_muc"])
    nguong = min(tu for tu, _, bu in policy["bac"] if bu > 0)
    return {"phut_tre": phut, "muc_bu": muc, "nguong": nguong,
            "ly_do": "trễ %d phút so với giờ dự kiến" % phut if phut > 0 else "giao đúng hoặc sớm hơn giờ dự kiến"}


@tool
def draft_voucher(ma_don: str, so_tien: int, ly_do: str) -> dict:
    """draft_voucher · input: mã đơn, số tiền, lý do · output: bản nháp voucher trạng thái "cho_duyet"
    · CÓ tác động ra ngoài nếu phát thật → ở đây CHỈ tạo bản nháp, nhân viên duyệt mới phát."""
    return {"ma_don": ma_don, "so_tien": so_tien, "ly_do": ly_do, "trang_thai": "cho_duyet"}


@tool
def escalate_to_human(ma_don: str, tom_tat: str) -> dict:
    """escalate_to_human · input: mã đơn (có thể rỗng), tóm tắt · output: ca chờ nhân viên
    · có tác động ra ngoài (tạo ca) — đảo được, nhân viên đóng ca. Ở bản chạy thử chỉ trả ca giả."""
    return {"ma_don": ma_don, "tom_tat": tom_tat, "trang_thai": "cho_nhan_vien"}
