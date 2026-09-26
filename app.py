from flask import Flask, render_template_string, request, redirect
import json, os

app = Flask(__name__)
DATA_FILE = "accounts.json"

def load_accounts():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_accounts(acc):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(acc, f, ensure_ascii=False)

HTML = """
<!DOCTYPE html>
<html dir="rtl">
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{font-family:Arial;background:#f5f5f5;padding:10px}
.card{background:white;padding:15px;border-radius:10px;margin:10px 0;box-shadow:0 2px 5px #ccc}
.btn{padding:10px 15px;border:none;border-radius:5px;color:white;margin:5px;cursor:pointer}
.green{background:#27ae60}.blue{background:#2980b9}.red{background:#c0392b}.orange{background:#e67e22}
input{padding:8px;margin:5px;width:90%;border:1px solid #ddd;border-radius:5px}
h2{text-align:center;color:#2c3e50}
.frozen{border-right:5px solid red;background:#ffeaea}
.active{border-right:5px solid green}
</style>
</head>
<body>
<h2>🏦 Al-Khalifi Bank System V5<br>نظام الخليفي المصرفي</h2>

<div class="card">
<h3>➕ فتح حساب جديد</h3>
<form action="/add" method="post">
<input name="id" placeholder="رقم الحساب مثلا 101" required>
<input name="name" placeholder="الاسم مثلا وفاء" required>
<input name="balance" type="number" placeholder="الرصيد الاول" required>
<input name="password" type="password" placeholder="كلمة السر" required>
<button class="btn green" type="submit">فتح الحساب</button>
</form>
</div>

<div class="card">
<h3>💸 عمليات (إيداع / سحب / تحويل)</h3>
<form action="/trans" method="post">
<input name="id" placeholder="من حساب رقم" required>
<input name="to_id" placeholder="إلى حساب رقم (للتحويل فقط)">
<input name="amount" type="number" placeholder="المبلغ" required>
<input name="password" type="password" placeholder="كلمة السر" required>
<button class="btn blue" name="type" value="withdraw">سحب</button>
<button class="btn green" name="type" value="deposit">إيداع</button>
<button class="btn orange" name="type" value="transfer">تحويل</button>
</form>
</div>

<h3>📋 الحسابات</h3>
{% for id, acc in accounts.items() %}
<div class="card {{ 'frozen' if acc['status']!='نشط' else 'active' }}">
<b>#{{id}} - {{acc['name']}}</b><br>
الحالة: {{acc['status']}} - الرصيد: {{acc['balance']}} د.ل
{% if acc['status']!='نشط' %}<br><span style="color:red">🔒 مجمد تلقائيا - سحب مشبوه</span>{% endif %}
</div>
{% endfor %}

<div class="card">
<h3>🔒 سجل الأمان</h3>
{% for log in logs[-5:][::-1] %}<div>{{log}}</div>{% endfor %}
</div>

</body>
</html>
"""

accounts = load_accounts()
logs = []

@app.route("/")
def home():
    return render_template_string(HTML, accounts=accounts, logs=logs)

@app.route("/add", methods=["POST"])
def add():
    id = request.form["id"]
    accounts[id] = {"name": request.form["name"], "balance": float(request.form["balance"]), "password": request.form["password"], "status": "نشط"}
    save_accounts(accounts)
    logs.append(f"تم فتح حساب {id} باسم {request.form['name']}")
    return redirect("/")

@app.route("/trans", methods=["POST"])
def trans():
    id = request.form["id"]
    to_id = request.form.get("to_id")
    amount = float(request.form["amount"])
    pwd = request.form["password"]
    type_ = request.form["type"]

    if id not in accounts or accounts[id]["password"]!= pwd:
        logs.append(f"❌ محاولة دخول فاشلة لحساب {id}")
        return redirect("/")

    if type_ == "deposit":
        accounts[id]["balance"] += amount
        logs.append(f"إيداع {amount} في حساب {id}")
    elif type_ == "withdraw":
        if amount > 5000:
            accounts[id]["status"] = "مجمد"
            logs.append(f"🚨 تجميد حساب {id} - سحب مشبوه {amount}")
        else:
            accounts[id]["balance"] -= amount
            logs.append(f"سحب {amount} من حساب {id}")
    elif type_ == "transfer":
        if to_id not in accounts:
            logs.append(f"❌ حساب المستقبل {to_id} غير موجود")
            return redirect("/")
        if amount > 5000:
            accounts[id]["status"] = "مجمد"
            logs.append(f"🚨 تجميد حساب {id} - تحويل مشبوه {amount}")
        else:
            accounts[id]["balance"] -= amount
            accounts[to_id]["balance"] += amount
            logs.append(f"تحويل {amount} من {id} إلى {to_id}")

    save_accounts(accounts)
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
