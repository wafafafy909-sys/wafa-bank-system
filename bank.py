import json
from datetime import datetime, date

class Bank:
    def __init__(self):
        self.accounts = {
            "101": {"name": "وفاء - رئيسي", "balance": 15000, "status": "نشط", "tx": []},
            "102": {"name": "محمد احمد", "balance": 8000, "status": "نشط", "tx": []},
            "103": {"name": "سارة علي", "balance": 1200, "status": "نشط", "tx": []}
        }
        self.logs = []

    def check_auto_freeze(self, acc_id, amount, type_op):
        acc = self.accounts[acc_id]
        today = date.today().isoformat()
        # تجميد لو سحب اكثر من 5000
        if type_op == "سحب" and amount > 5000:
            acc["status"] = "مجمد تلقائيا - سحب كبير"
            self.logs.append(f"🚨 تجميد {acc_id} - سحب {amount} > 5000")
            return True
        # تجميد لو 3 سحوبات في نفس اليوم
        today_ops = [t for t in acc["tx"] if t["date"].startswith(today) and t["type"] == "سحب"]
        if type_op == "سحب" and len(today_ops) >= 2:
            acc["status"] = "مجمد - نشاط مشبوه"
            self.logs.append(f"🚨 تجميد {acc_id} - 3 سحوبات في نفس اليوم")
            return True
        return False

    def do_transaction(self, acc_id, amount, type_op):
        if acc_id not in self.accounts:
            return "الحساب مش موجود"
        acc = self.accounts[acc_id]
        if acc["status"] != "نشط":
            return f"الحساب مجمد: {acc['status']}"
        if self.check_auto_freeze(acc_id, amount, type_op):
            return "تم التجميد التلقائي!"
        if type_op == "سحب":
            if acc["balance"] < amount:
                return "الرصيد لا يكفي"
            acc["balance"] -= amount
        else:
            acc["balance"] += amount
        acc["tx"].append({"type": type_op, "amount": amount, "date": datetime.now().isoformat()})
        return "تمت العملية بنجاح ✅"
