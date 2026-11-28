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
import ai  # noqa: E402

PORT = int(os.environ.get("PORT", "8000"))

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
</style></head><body><div class="wrap">
<div class="top"><div><div class="kick">AI20K / BaChangLinhNguLam</div><h1>Trợ lý đơn giao trễ</h1></div>
<div class="badge" id="model">Model: __MODEL__</div></div>
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
const j=await r.json();w.remove();add('bot',j.output||('Lỗi: '+j.error),j.meta)}catch(e){w.remove();add('bot','Lỗi kết nối: '+e)}
send.disabled=false;q.focus()}
send.onclick=go;q.addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();go()}});
document.querySelectorAll('.ex').forEach(b=>b.onclick=()=>{q.value=b.dataset.q;q.focus()});
document.getElementById('reset').onclick=hello;hello();
</script></body></html>"""


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype):
        data = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype + "; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self._send(200, PAGE.replace("__MODEL__", ai.MODEL_NAME if ai.MODEL_PROVIDER != "fake" else "chế độ giả"), "text/html")
        else:
            self._send(404, "not found", "text/plain")

    def do_POST(self):
        if self.path != "/api/chat":
            return self._send(404, "{}", "application/json")
        try:
            n = int(self.headers.get("Content-Length", "0"))
            text = json.loads(self.rfile.read(n).decode("utf-8")).get("text", "")
            out = answer(text)["output"]
            self._send(200, json.dumps({"output": out}, ensure_ascii=False), "application/json")
        except Exception as e:  # lỗi model / mạng → báo lên giao diện
            self._send(500, json.dumps({"error": "%s: %s" % (type(e).__name__, e)}, ensure_ascii=False), "application/json")

    def log_message(self, fmt, *args):
        sys.stderr.write("[web] " + fmt % args + "\n")


if __name__ == "__main__":
    print("Mở http://localhost:%d  (model: %s)" % (PORT, ai.MODEL_NAME or ai.MODEL_PROVIDER))
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
