# Wafa Bank System - منظومة مصرفية
# Student: Wafa Talbi

class BankAccount:
    def __init__(self, account_number, name, balance=0):
        self.account_number = account_number
        self.name = name
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print(f"تم ايداع {amount} - الرصيد الجديد: {self.balance}")

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            print(f"تم السحب {amount} - الرصيد الجديد: {self.balance}")
        else:
            print("رصيدك لا يكفي!")

    def check_balance(self):
        print(f"صاحب الحساب: {self.name} - الرصيد: {self.balance}")

# قائمة الحسابات
accounts = {}

def create_account():
    acc_num = input("ادخلي رقم الحساب: ")
    name = input("ادخلي اسم العميل: ")
    balance = float(input("ادخلي الرصيد الابتدائي: "))
    accounts[acc_num] = BankAccount(acc_num, name, balance)
    print("تم انشاء الحساب بنجاح!")

def main():
    while True:
        print("\n--- Wafa Bank System ---")
        print("1. انشاء حساب جديد")
        print("2. ايداع")
        print("3. سحب")
        print("4. كشف رصيد")
        print("5. خروج")
        
        choice = input("اختاري: ")
        
        if choice == "1":
            create_account()
        elif choice == "2":
            acc_num = input("رقم الحساب: ")
            amount = float(input("المبلغ: "))
            if acc_num in accounts:
                accounts[acc_num].deposit(amount)
            else:
                print("الحساب غير موجود")
        elif choice == "3":
            acc_num = input("رقم الحساب: ")
            amount = float(input("المبلغ: "))
            if acc_num in accounts:
                accounts[acc_num].withdraw(amount)
            else:
                print("الحساب غير موجود")
        elif choice == "4":
            acc_num = input("رقم الحساب: ")
            if acc_num in accounts:
                accounts[acc_num].check_balance()
            else:
                print("الحساب غير موجود")
        elif choice == "5":
            print("شكرا لاستخدامك منظومة وفاء المصرفية")
            break

main()
