"""Giao diện web cho demo: python codebase/web.py → mở http://localhost:8000

Chỉ dùng thư viện chuẩn. Mỗi tin nhắn gửi vào answer() trong agent.py (cùng luồng với `python run.py`).
"""
import json
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agent import answer  # noqa: E402
import tools  # noqa: E402
import ai  # noqa: E402

PORT = int(os.environ.get("PORT", "8000"))
PENDING = {}   # mã đơn → kết quả phân tích lần chat gần nhất (server giữ, không tin số tiền từ trình duyệt)

PAGE = """<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Trợ lý đơn giao trễ</title>
<style>
*{box-sizing:border-box}body{margin:0;font-family:"Segoe UI",Arial,sans-serif;background:#f3f1ec;color:#1d2b26}
.wrap{max-width:1120px;margin:0 auto;padding:28px 24px}
.top{display:flex;justify-content:space-between;align-items:flex-end;margin-bottom:22px}
.kick{color:#b5452a;font-weight:700;font-size:14px}h1{margin:6px 0 0;font-size:44px}
.badge{border:1px solid #d8d4ca;background:#fff;border-radius:8px;padding:8px 12px;font-size:14px;color:#4a564f}
.grid{display:grid;grid-template-columns:250px 1fr;gap:20px}
.card{background:#fff;border:1px solid #e3dfd5;border-radius:14px}
.side{padding:18px}.side h2{font-size:17px;margin:0 0 6px}.side p{font-size:14px;color:#5b665f;margin:0 0 12px}
.ex{display:block;width:100%;text-align:left;border:1px solid #e3dfd5;background:#f6f4ef;border-radius:10px;padding:10px 12px;margin-bottom:10px;cursor:pointer;font:inherit}
.ex b{display:block;font-size:14.5px}.ex span{font-size:13.5px;color:#5b665f}
.chat{display:flex;flex-direction:column;height:600px}
.head{display:flex;justify-content:space-between;align-items:center;padding:16px 20px;border-bottom:1px solid #e3dfd5;font-weight:700}
.head button{border:0;background:none;color:#1f5c4b;font-weight:700;cursor:pointer;font-size:15px}
.log{flex:1;overflow:auto;padding:16px 20px}
.msg{margin-bottom:14px}.who{font-size:13px;font-weight:700;color:#4a564f;margin-bottom:4px}
.bub{display:inline-block;max-width:78%;padding:11px 15px;border-radius:12px;line-height:1.5;font-size:15.5px;white-space:pre-wrap}
.bot .bub{background:#e5efe9}.me{text-align:right}.me .bub{background:#1f5c4b;color:#fff;text-align:left}
.meta{font-size:12px;color:#8a938d;margin-top:4px}
.form{border-top:1px solid #e3dfd5;padding:14px 20px;display:flex;gap:12px;align-items:flex-end}
.form label{display:block;font-size:14px;font-weight:700;margin-bottom:6px}
textarea{width:100%;height:64px;border:1px solid #d8d4ca;border-radius:8px;padding:10px;font:inherit;resize:vertical}
.send{background:#1f5c4b;color:#fff;border:0;border-radius:8px;padding:12px 18px;font-weight:700;cursor:pointer;font-size:15px}
.send:disabled{opacity:.5}
.fcard{border:1px solid #cfe0d7;background:#f7fbf9;border-radius:12px;padding:14px 16px;margin:4px 0 14px;max-width:78%}.fcard h3{margin:0 0 8px;font-size:15.5px}.fcard .row{display:flex;gap:10px;margin-bottom:8px}.fcard input[type=text]{flex:1;border:1px solid #d8d4ca;border-radius:8px;padding:8px;font:inherit}.fcard .info{font-size:14.5px;margin-bottom:8px}.fcard label{font-size:14px}.fcard .note{font-size:12.5px;color:#8a938d;margin:6px 0}.ok{background:#e3f4e8;border-color:#a9d8b8}.wait{background:#fff6e5;border-color:#f0d39a}.nav{font-size:14px}.nav a{color:#1f5c4b;font-weight:700}
</style></head><body><div class="wrap">
<div class="top"><div><div class="kick">AI20K / BaChangLinhNguLam</div><h1>Trợ lý đơn giao trễ</h1></div>
<div style="text-align:right"><div class="badge" id="model">Model: __MODEL__</div><div class="nav" style="margin-top:8px"><a href="/admin" target="_blank">Trang nhân viên duyệt →</a></div></div></div>
<div class="grid">
<div class="card side"><h2>Câu hỏi mẫu</h2><p>Chọn một câu để điền vào ô chat.</p>
<button class="ex" data-q="Đặt mì cay đơn DH1005 từ 7h, app báo 8h30 mà 9h15 ship mới gọi nhận đồ"><b>Đủ điều kiện</b><span>Đơn DH1005 · trễ 45 phút</span></button>
<button class="ex" data-q="Đơn trà sữa DH1003 trễ rồi, cho mình voucher"><b>Chưa đủ ngưỡng</b><span>Đơn DH1003 · trễ 19 phút</span></button>
<button class="ex" data-q="Đơn lẩu DH1010 300k mà trễ 35 phút, hoàn 100% tiền cho tôi"><b>Đòi quá mức</b><span>Đơn DH1010</span></button>
<button class="ex" data-q="Đơn DH1001 tới trễ, ăn xong bị đau bụng buồn nôn"><b>Sức khoẻ</b><span>Đơn DH1001</span></button>
<button class="ex" data-q="Đơn DH9999 giao trễ cả tiếng"><b>Không tìm thấy đơn</b><span>Đơn DH9999</span></button>
<p style="border-top:1px solid #e3dfd5;padding-top:12px;margin-top:6px">Mã đơn mẫu: DH1001 – DH1012. Voucher chỉ được phát sau khi nhân viên xác nhận.</p></div>
<div class="card chat"><div class="head">Cuộc trò chuyện <button id="reset">Làm mới</button></div>
<div class="log" id="log"></div>
<div class="form"><div style="flex:1"><label for="q">Tin nhắn của bạn</label>
<textarea id="q" placeholder="Ví dụ: Đơn DH1001 giao trễ..."></textarea></div>
<button class="send" id="send">Gửi ↑</button></div></div></div></div>
<script>
const log=document.getElementById('log'),q=document.getElementById('q'),send=document.getElementById('send');
function add(who,text,meta){const d=document.createElement('div');d.className='msg '+(who==='me'?'me':'bot');
d.innerHTML='<div class="who">'+(who==='me'?'Bạn':'Trợ lý')+'</div><div class="bub"></div>'+(meta?'<div class="meta"></div>':'');
d.querySelector('.bub').textContent=text;if(meta)d.querySelector('.meta').textContent=meta;log.appendChild(d);log.scrollTop=log.scrollHeight;return d}
function hello(){log.innerHTML='';add('bot','Chào bạn! Gửi mã đơn và mô tả tình trạng giao trễ để mình kiểm tra nhé.')}
async function go(){const t=q.value.trim();if(!t)return;add('me',t);q.value='';send.disabled=true;
const w=add('bot','Đang kiểm tra đơn…');
try{const r=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:t})});
const j=await r.json();w.remove();add('bot',j.output||('Lỗi: '+j.error),j.meta);if(j.action==='de_xuat_voucher')form(j)}catch(e){w.remove();add('bot','Lỗi kết nối: '+e)}
send.disabled=false;q.focus()}
function vnd(x){return x.toLocaleString('vi-VN')+'đ'}
function form(j){const d=document.createElement('div');d.className='fcard';
d.innerHTML='<h3>Xác nhận yêu cầu bù giao trễ</h3><div class="info">Đơn <b>'+j.ma_don+'</b> · trễ <b>'+j.phut_tre+' phút</b> · voucher đề xuất <b>'+vnd(j.muc_bu)+'</b></div>'+
'<div class="row"><input type="text" class="hn" placeholder="Họ tên"><input type="text" class="sdt" placeholder="Số điện thoại nhận thông báo"></div>'+
'<label><input type="checkbox" class="ok1"> Tôi xác nhận đơn bị giao trễ như trên và đồng ý nhận voucher theo chính sách bù giao trễ.</label>'+
'<div class="note">Bản demo: dùng tên / số giả, không nhập thông tin thật.</div><button class="send">Xác nhận gửi yêu cầu</button>';
log.appendChild(d);log.scrollTop=log.scrollHeight;
d.querySelector('button').onclick=async()=>{const hn=d.querySelector('.hn').value.trim(),sdt=d.querySelector('.sdt').value.trim();
if(!hn||!sdt||!d.querySelector('.ok1').checked){alert('Điền họ tên, số điện thoại và tick đồng ý nhé.');return}
const r=await fetch('/api/confirm',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({ma_don:j.ma_don,ho_ten:hn,sdt:sdt})});
const k=await r.json();if(k.error){alert(k.error);return}
d.className='fcard '+(k.trang_thai==='cho_nhan_vien'?'wait':'ok');
d.innerHTML='<h3>Phiếu '+k.ma_phieu+(k.trung?' (đã gửi trước đó)':'')+'</h3><div class="info">'+k.thong_bao+'</div>';log.scrollTop=log.scrollHeight}}
send.onclick=go;q.addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();go()}});
document.querySelectorAll('.ex').forEach(b=>b.onclick=()=>{q.value=b.dataset.q;q.focus()});
document.getElementById('reset').onclick=hello;hello();
</script></body></html>"""


import csv as _csv
import html as _html

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Chỉ những file này được mở để xem (không mở file tuỳ ý)
DATASETS = {
    "cau-thu":    ("Bộ 20 câu thử", "eval/benchmark.csv", "Câu khách nhắn, kết quả đúng, tiêu chí đạt, loại câu, nguồn."),
    "luot-1":     ("Kết quả lượt 1 (14/20)", "eval/run-1.csv", "Output thật của model, cột pass (1 = đạt), ghi chú vì sao."),
    "luot-3":     ("Kết quả lượt 3 (20/20)", "eval/run-3.csv", "Sau cải tiến và sửa lỗi bước kiểm."),
    "luot-5":     ("Kết quả lượt 5 (20/20, bản cuối)", "eval/run-5.csv", "Bản có form xác nhận + tự duyệt."),
    "review":     ("150 review ShopeeFood (Google Play)", "evidence/reviews-shopeefood.csv", "Mỗi review: ngày, số sao, trích ngắn, nhãn. Không có tên người viết."),
    "khao-sat":   ("Khảo sát — 23 phiếu", "evidence/survey/results.csv", "Câu trả lời thật, ẩn danh."),
    "don-hang":   ("12 đơn hàng mẫu (dữ liệu giả)", "data/don_hang.csv", "Dùng cho bản chạy thử và bộ câu thử."),
    "chinh-sach": ("Chính sách bù giao trễ (tự đặt)", "data/chinh_sach.csv", "Bậc bù theo phút trễ, hạn mức."),
    "lich-su":    ("Lịch sử khiếu nại (dữ liệu giả)", "data/lich_su_khieu_nai.csv", "Số lần khiếu nại giao trễ trong 30 ngày."),
    "chi-phi":    ("Mô phỏng chi phí — 50 phiên", "cost/simulate-1.csv", "Token đo thật từng phiên."),
}
HIDE_COLS = {"run_id", "model", "model_calls", "tool_calls", "tokens_in", "tokens_out", "latency_s", "error",
             "expected", "pass_criterion"}


def view_page(key):
    if key not in DATASETS:
        links = "".join('<li><a href="/xem/%s">%s</a> — %s</li>' % (k, t, d) for k, (t, _, d) in DATASETS.items())
        return VIEW_HTML.replace("__TITLE__", "Dữ liệu của nhóm").replace("__DESC__", "Chọn một bộ dữ liệu.") \
            .replace("__BODY__", "<ul class='list'>%s</ul>" % links).replace("__COUNT__", "")
    title, rel, desc = DATASETS[key]
    with open(os.path.join(ROOT_DIR, rel), encoding="utf-8-sig") as f:
        rows = list(_csv.reader(f))
    head, data = rows[0], rows[1:]
    keep = [i for i, h in enumerate(head) if not (key.startswith("luot") and h in HIDE_COLS)]
    th = "".join("<th>%s</th>" % _html.escape(head[i]) for i in keep)
    trs = []
    for r in data:
        cells = []
        for i in keep:
            v = r[i] if i < len(r) else ""
            cls = ""
            if head[i] == "pass":
                cls, v = ("ok", "✔ đạt") if v == "1" else (("no", "✘ trượt") if v == "0" else ("", v))
            cells.append('<td class="%s">%s</td>' % (cls, _html.escape(v)))
        trs.append("<tr>%s</tr>" % "".join(cells))
    body = "<table id='t'><thead><tr>%s</tr></thead><tbody>%s</tbody></table>" % (th, "".join(trs))
    return VIEW_HTML.replace("__TITLE__", _html.escape(title)).replace("__DESC__", _html.escape(desc) + " · File: <code>%s</code>" % rel) \
        .replace("__BODY__", body).replace("__COUNT__", "%d dòng" % len(data))


VIEW_HTML = """<!doctype html><html lang="vi"><head><meta charset="utf-8"><title>__TITLE__</title>
<style>body{font-family:"Segoe UI",Arial,sans-serif;background:#f3f1ec;margin:0;padding:24px 28px;color:#1d2b26}
.k{font-size:14px;color:#b5452a;font-weight:700}h1{margin:4px 0}p{color:#5b665f;margin:4px 0 12px}
.bar{display:flex;gap:12px;align-items:center;margin-bottom:12px}input{flex:0 0 340px;padding:9px 12px;border:1px solid #d8d4ca;border-radius:8px;font:inherit}
table{border-collapse:collapse;width:100%;background:#fff}th,td{padding:8px 10px;border-bottom:1px solid #ece8df;text-align:left;font-size:14px;vertical-align:top}
th{background:#e9e5dc;position:sticky;top:0}tr:hover td{background:#faf8f3}.ok{color:#2b8a3e;font-weight:700}.no{color:#c92a2a;font-weight:700}
.list li{margin:8px 0;font-size:16px}a{color:#1f5c4b;font-weight:700}</style></head><body>
<div class="k">AI20K / BaChangLinhNguLam · <a href="/xem">tất cả dữ liệu</a> · <a href="/trinh-bay">slide</a> · <a href="/">trợ lý</a></div>
<h1>__TITLE__</h1><p>__DESC__</p>
<div class="bar"><input id="f" placeholder="Lọc nhanh: gõ mã câu, nhãn, từ khoá…" oninput="flt()"><span id="c">__COUNT__</span></div>
__BODY__
<script>function flt(){const q=document.getElementById('f').value.toLowerCase();let n=0;
document.querySelectorAll('#t tbody tr').forEach(r=>{const v=r.textContent.toLowerCase().includes(q);r.style.display=v?'':'none';if(v)n++});
const c=document.getElementById('c');if(document.getElementById('t'))c.textContent=n+' dòng'}</script></body></html>"""


STATUS_VI = {"da_duyet_tu_dong": "Đã duyệt tự động", "cho_nhan_vien": "Chờ nhân viên duyệt",
             "da_duyet": "Nhân viên đã duyệt", "tu_choi": "Nhân viên từ chối"}


def _vnd(x):
    return "{:,}".format(x).replace(",", ".") + "đ"


def admin_page():
    rows = tools.list_complaints()
    trs = []
    for r in reversed(rows):
        if r["trang_thai"] == "cho_nhan_vien":
            act = ('<button onclick="rv(\'%s\',\'duyet\')">Duyệt</button> '
                   '<button class="no" onclick="rv(\'%s\',\'tu_choi\')">Từ chối</button>') % (r["ma_phieu"], r["ma_phieu"])
        else:
            act = r.get("nguoi_duyet") or ""
        trs.append("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s phút</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
            r["ma_phieu"], r["tao_luc"], r["ma_don"], r["phut_tre"], _vnd(r["muc_bu"]), r["ho_ten"],
            STATUS_VI.get(r["trang_thai"], r["trang_thai"]), r["ly_do_duyet"], act))
    body = "".join(trs) or '<tr><td colspan="9">Chưa có phiếu nào.</td></tr>'
    return ADMIN_HTML.replace("__ROWS__", body)


ADMIN_HTML = """<!doctype html><html lang="vi"><head><meta charset="utf-8"><title>Bảng khiếu nại giao trễ</title>
<style>body{font-family:"Segoe UI",Arial,sans-serif;background:#f3f1ec;margin:0;padding:28px;color:#1d2b26}h1{margin:4px 0 6px}
p{color:#5b665f}table{border-collapse:collapse;width:100%;background:#fff}
th,td{padding:10px 12px;border-bottom:1px solid #e3dfd5;text-align:left;font-size:14.5px}th{background:#e9e5dc}
button{border:0;border-radius:6px;padding:6px 10px;cursor:pointer;font-weight:700;background:#1f5c4b;color:#fff}button.no{background:#e9e5dc;color:#1d2b26}</style></head>
<body><div style="font-size:14px;color:#b5452a;font-weight:700">AI20K / BaChangLinhNguLam · trang nhân viên</div><h1>Bảng khiếu nại giao trễ</h1>
<p>Tự duyệt khi voucher ≤ 15.000đ và khách chưa khiếu nại lần nào trong 30 ngày (luật bằng code, không do AI quyết). Còn lại nhân viên duyệt ở đây. Trang tự làm mới mỗi 10 giây.</p>
<table><tr><th>Phiếu</th><th>Tạo lúc</th><th>Đơn</th><th>Trễ</th><th>Voucher</th><th>Khách</th><th>Trạng thái</th><th>Lý do</th><th>Duyệt</th></tr>__ROWS__</table>
<script>async function rv(id,q){await fetch('/api/review',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({ma_phieu:id,quyet_dinh:q})});location.reload()}
setTimeout(()=>location.reload(),10000)</script></body></html>"""


def confirm(body):
    """Khách xác nhận → luật code quyết tự duyệt hay chờ nhân viên → lưu phiếu."""
    res = PENDING.get((body.get("ma_don") or "").upper())
    if not res:
        return {"error": "Chưa có đề xuất voucher cho đơn này — hãy nhắn trợ lý trước."}
    if not (body.get("ho_ten") or "").strip() or not (body.get("sdt") or "").strip():
        return {"error": "Thiếu họ tên hoặc số điện thoại."}
    rule = tools.check_auto_approve(res["muc_bu"], res["so_lan_30_ngay"], res["co_van_de_khac"])
    rec = tools.save_complaint(res["ma_don"], res["ma_khach"], res["phut_tre"], res["muc_bu"],
                               body["ho_ten"].strip()[:60], body["sdt"].strip()[:20], rule["tu_duyet"], rule["ly_do"])
    tien = _vnd(rec["muc_bu"])
    if rec["trang_thai"] == "da_duyet_tu_dong":
        msg = "Voucher %s đã được duyệt tự động và gửi vào ví voucher của bạn (%s)." % (tien, rec["ly_do_duyet"])
    elif rec["trang_thai"] == "cho_nhan_vien":
        msg = ("Yêu cầu voucher %s đã được ghi nhận và đang chờ nhân viên duyệt (%s). "
               "Bạn sẽ nhận thông báo khi có kết quả." % (tien, rec["ly_do_duyet"]))
    else:
        msg = "Phiếu này đã được xử lý: %s." % STATUS_VI.get(rec["trang_thai"], rec["trang_thai"])
    return dict(rec, thong_bao=msg)


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype):
        data = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype + "; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path.startswith("/xem"):
            key = self.path[len("/xem"):].strip("/").split("?")[0]
            return self._send(200, view_page(key), "text/html")
        if self.path.startswith("/trinh-bay"):
            with open(os.path.join(ROOT_DIR, "slides", "trinh-bay.html"), encoding="utf-8") as f:
                return self._send(200, f.read(), "text/html")
        if self.path.startswith("/admin"):
            return self._send(200, admin_page(), "text/html")
        if self.path in ("/", "/index.html"):
            self._send(200, PAGE.replace("__MODEL__", ai.MODEL_NAME if ai.MODEL_PROVIDER != "fake" else "chế độ giả"), "text/html")
        else:
            self._send(404, "not found", "text/plain")

    def do_POST(self):
        try:
            n = int(self.headers.get("Content-Length", "0"))
            body = json.loads(self.rfile.read(n).decode("utf-8") or "{}")
            if self.path == "/api/chat":
                res = answer(body.get("text", ""))
                if res.get("action") == "de_xuat_voucher":
                    PENDING[res["ma_don"]] = res
                return self._send(200, json.dumps(res, ensure_ascii=False), "application/json")
            if self.path == "/api/confirm":
                return self._send(200, json.dumps(confirm(body), ensure_ascii=False), "application/json")
            if self.path == "/api/review":
                out = tools.review_complaint(body.get("ma_phieu", ""), body.get("quyet_dinh", ""))
                return self._send(200, json.dumps(out, ensure_ascii=False), "application/json")
            self._send(404, "{}", "application/json")
        except Exception as e:  # lỗi model / mạng → báo lên giao diện
            self._send(500, json.dumps({"error": "%s: %s" % (type(e).__name__, e)}, ensure_ascii=False), "application/json")

    def log_message(self, fmt, *args):
        sys.stderr.write("[web] " + fmt % args + "\n")


if __name__ == "__main__":
    print("Mở http://localhost:%d  (model: %s)" % (PORT, ai.MODEL_NAME or ai.MODEL_PROVIDER))
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
