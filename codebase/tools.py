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
def escalate_to_human(ma_don: str, tom_tat: str, loai: str = "khac", tin_nhan: str = "", tro_ly_da_noi: str = "") -> dict:
    """escalate_to_human · input: mã đơn (có thể rỗng), tóm tắt, loại ca (suc_khoe | da_huy | nhieu_lan | ngoai_pham_vi),
    tin nhắn gốc, trợ lý đã nói gì · output: ca chờ nhân viên (ca sức khoẻ ưu tiên KHẨN)
    · có tác động: tạo ca trong hàng chờ nhân viên — đảo được, nhân viên đóng ca.
    Chỉ lưu vào bảng khi chạy giao diện web (biến môi trường WEB_DEMO=1); lúc chạy eval / simulate chỉ trả ca, không ghi."""
    ca = {"ma_don": ma_don, "tom_tat": tom_tat, "loai": loai, "uu_tien": "khan" if loai == "suc_khoe" else "thuong",
          "trang_thai": "cho_nhan_vien"}
    if os.environ.get("WEB_DEMO") != "1":
        return ca
    order = {}
    for row in _read("don_hang.csv"):
        if row["ma_don"].upper() == (ma_don or "").upper():
            order = row
    ca.update(kieu="chuyen_nhan_vien", quan=order.get("quan", ""), gio_giao=order.get("gio_giao_thuc_te", ""),
              gia_tri=order.get("tong_tien", ""), tin_nhan=tin_nhan[:300], tro_ly_da_noi=tro_ly_da_noi,
              tao_luc=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    with _LOCK_ESC:
        rows = _load()
        ca["ma_phieu"] = "CA%04d" % (sum(1 for r in rows if r.get("kieu") == "chuyen_nhan_vien") + 1)
        rows.append(ca)
        _save(rows)
    return ca


# ---- Bảng khiếu nại + duyệt (thêm sau CP4) ----------------------------------------
# Lưu ở data/runtime/khieu_nai.json — dữ liệu lúc chạy, KHÔNG commit (đã thêm vào .gitignore).
import json as _json
import threading as _threading

AUTO_APPROVE_MAX = 15000          # tự duyệt khi mức bù ≤ 15.000đ …
AUTO_APPROVE_MAX_HISTORY = 0      # … và khách chưa khiếu nại giao trễ lần nào trong 30 ngày
_RUNTIME = os.path.join(DATA, "runtime", "khieu_nai.json")
_LOCK = _threading.Lock()
_LOCK_ESC = _LOCK


def _load():
    if not os.path.exists(_RUNTIME):
        return []
    with open(_RUNTIME, encoding="utf-8") as f:
        return _json.load(f)


def _save(rows):
    os.makedirs(os.path.dirname(_RUNTIME), exist_ok=True)
    with open(_RUNTIME, "w", encoding="utf-8") as f:
        _json.dump(rows, f, ensure_ascii=False, indent=2)


@tool
def check_auto_approve(muc_bu: int, so_lan_30_ngay: int, co_van_de_khac: bool) -> dict:
    """check_auto_approve · input: mức bù code đã tính, số lần khiếu nại 30 ngày, có vấn đề ngoài phạm vi / đòi thêm không
    · output: {"tu_duyet": bool, "ly_do": str} — LUẬT CỨNG BẰNG CODE, AI không quyết · không tác động ra ngoài."""
    if muc_bu <= 0:
        return {"tu_duyet": False, "ly_do": "không có mức bù"}
    if muc_bu > AUTO_APPROVE_MAX:
        return {"tu_duyet": False, "ly_do": "mức bù trên %sđ cần nhân viên duyệt" % "{:,}".format(AUTO_APPROVE_MAX).replace(",", ".")}
    if so_lan_30_ngay > AUTO_APPROVE_MAX_HISTORY:
        return {"tu_duyet": False, "ly_do": "khách đã khiếu nại trong 30 ngày, cần nhân viên duyệt"}
    if co_van_de_khac:
        return {"tu_duyet": False, "ly_do": "có yêu cầu ngoài phạm vi / đòi thêm, cần nhân viên duyệt"}
    return {"tu_duyet": True, "ly_do": "mức bù nhỏ, khách chưa khiếu nại lần nào trong 30 ngày"}


@tool
def save_complaint(ma_don: str, ma_khach: str, phut_tre: int, muc_bu: int, ho_ten: str, sdt: str,
                   tu_duyet: bool, ly_do_duyet: str) -> dict:
    """save_complaint · input: thông tin đơn (code tính) + thông tin khách xác nhận · output: phiếu khiếu nại
    · CÓ tác động: ghi vào bảng khiếu nại (data/runtime/khieu_nai.json). Mỗi đơn chỉ một phiếu.
    Tự duyệt chỉ khi check_auto_approve cho phép; còn lại trạng thái "cho_nhan_vien"."""
    with _LOCK:
        rows = _load()
        for r in rows:
            if r["ma_don"] == ma_don and r.get("kieu") != "chuyen_nhan_vien":
                return dict(r, trung=True)
        rec = {"ma_phieu": "KN%04d" % (sum(1 for r in rows if r.get("kieu") != "chuyen_nhan_vien") + 1), "ma_don": ma_don, "ma_khach": ma_khach,
               "phut_tre": phut_tre, "muc_bu": muc_bu, "ho_ten": ho_ten, "sdt": sdt,
               "trang_thai": "da_duyet_tu_dong" if tu_duyet else "cho_nhan_vien",
               "ly_do_duyet": ly_do_duyet, "tao_luc": datetime.now().strftime(TIME_FMT), "nguoi_duyet": "he_thong" if tu_duyet else ""}
        rows.append(rec)
        _save(rows)
        return rec


@tool
def list_complaints() -> list:
    """list_complaints · input: không · output: mọi phiếu khiếu nại · không tác động ra ngoài."""
    return _load()


@tool
def review_complaint(ma_phieu: str, quyet_dinh: str, nguoi_duyet: str = "nhan_vien") -> dict:
    """review_complaint · input: mã phiếu, quyết định ("duyet" | "tu_choi") · output: phiếu đã cập nhật
    · CÓ tác động: NHÂN VIÊN duyệt / từ chối phiếu đang chờ (không dành cho AI)."""
    with _LOCK:
        rows = _load()
        for r in rows:
            if r.get("ma_phieu") == ma_phieu and r["trang_thai"] == "cho_nhan_vien":
                if r.get("kieu") == "chuyen_nhan_vien":
                    r["trang_thai"] = "da_xu_ly"
                else:
                    r["trang_thai"] = "da_duyet" if quyet_dinh == "duyet" else "tu_choi"
                r["nguoi_duyet"] = nguoi_duyet
                r["duyet_luc"] = datetime.now().strftime(TIME_FMT)
                _save(rows)
                return r
    return {"loi": "không tìm thấy phiếu đang chờ %s" % ma_phieu}
