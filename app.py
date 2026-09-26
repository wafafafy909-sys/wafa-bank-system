from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)
balance = 1000

HTML = """
<h2 style="text-align:center; font-family:Tahoma">🏦 نظام وفاء المصرفي</h2>
<div style="max-width:400px;margin:auto; font-family:Tahoma; background:#f9f9f9; padding:20px; border-radius:10px">
<p><b>رصيدك الحالي: {{balance}} دينار</b></p>
<form method="post">
<input name="amount" type="number" placeholder="المبلغ" required style="width:100%;padding:8px"><br><br>
<button name="action" value="deposit" style="width:48%;padding:10px;background:green;color:white">إيداع</button>
<button name="action" value="withdraw" style="width:48%;padding:10px;background:red;color:white">سحب</button>
</form>
<p style="color:{{color}}">{{msg}}</p>
</div>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    global balance
    msg = ""
    color = "black"
    if request.method == "POST":
        try:
            amount = int(request.form["amount"])
            action = request.form["action"]
            if action == "deposit":
                balance += amount
                msg = f"تم إيداع {amount} بنجاح"
                color = "green"
            else:
                if balance >= amount:
                    balance -= amount
                    msg = f"تم سحب {amount} بنجاح"
                    color = "red"
                else:
                    msg = "رصيدك لا يكفي!"
                    color = "red"
        except:
            msg = "اكتبي رقم صحيح"
    return render_template_string(HTML, balance=balance, msg=msg, color=color)

if __name__ == "__main__":
    app.run()
