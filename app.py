from flask import Flask, request
from bank import Bank

app = Flask(__name__)
bank = Bank()

@app.route("/", methods=["GET", "POST"])
def home():
    msg = ""
    if request.method == "POST":
        acc_id = request.form.get("acc")
        amount = float(request.form.get("amount") or 0)
        typ = request.form.get("typ")
        msg = bank.do_transaction(acc_id, amount, typ)
    
    html = ""
    for id, a in bank.accounts.items():
        color = "green" if a["status"] == "نشط" else "red"
        html += f'<div style="border-right:6px solid {color};background:#fff;padding:12px;margin:10px;border-radius:10px;color:#000"><b>{a["name"]} #{id}</b><br>الحالة: {a["status"]} - الرصيد: {a["balance"]} د.ل</div>'

    logs_html = "<br>".join(bank.logs[::-1]) if bank.logs else "لا يوجد تنبيهات ✅"

    return f"""
    <html dir="rtl"><body style="font-family:Arial;background:#f0f2f5;padding:20px">
    <h1 style="text-align:center;color:#000">🏦 منظومة وفاء V4 - التجميد التلقائي</h1>
    <form method="post" style="background:#fff;padding:15px;border-radius:12px;text-align:center">
    <input name="acc" placeholder="رقم الحساب 101" style="padding:10px;width:25%">
    <input name="amount" type="number" placeholder="المبلغ" style="padding:10px;width:25%">
    <button name="typ" value="ايداع" style="padding:10px;background:green;color:#fff;border:none;border-radius:8px">ايداع</button>
    <button name="typ" value="سحب" style="padding:10px;background:blue;color:#fff;border:none;border-radius:8px">سحب</button>
    </form>
    <h3 style="color:blue;text-align:center">{msg}</h3>
    {html}
    <div style="background:#fff;padding:15px;margin-top:20px;border-radius:10px;color:#000"><h3>سجل الأمان 🔒</h3>{logs_html}</div>
    </body></html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
