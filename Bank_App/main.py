import mysql.connector
import time
from datetime import datetime

# DB connection
db = mysql.connector.connect(
    host="localhost",  # or your server host
    user="root",  # your username
    password="Aditya@2002",  # Replace with your MySQL password
    database="bankdb"
)
cursor = db.cursor()


def verify_password(acc_no):
    # Check if account exists
    cursor.execute("SELECT password FROM accounts WHERE acc_no = %s", (acc_no,))
    result = cursor.fetchone()

    if not result:
        print("❌ Account number not found.")
        return None

    attempts = 3
    while attempts > 0:
        passwd = input("Enter your password: ")
        if result[0] == passwd:
            return True
        else:
            attempts -= 1
            print(f"❌ Incorrect password. Attempts left: {attempts}")

    print("⏳ Too many failed attempts. Please wait 10 seconds...")
    time.sleep(10)
    return False



def create_account():
    name = input("Enter your name: ")
    password = input("Set a password: ")

    while True:
        dob_input = input("Enter your Date of Birth (YYYY-MM-DD): ")
        try:
            dob = datetime.strptime(dob_input, "%Y-%m-%d").date()
            break
        except ValueError:
            print("❗ Invalid date format. Please use YYYY-MM-DD.")

    balance = float(input("Enter initial deposit: "))

    sql = "INSERT INTO accounts (name, password, dob, balance) VALUES (%s, %s, %s, %s)"
    values = (name, password, dob, balance)

    try:
        cursor.execute(sql, values)
        db.commit()
        acc_no = cursor.lastrowid
        print(f"✅ Account created successfully! Your Account Number is: {acc_no}")
    except Exception as e:
        db.rollback()
        print("❌ Failed to create account:", e)


def check_balance():
    while True:
        try:
            acc_no = int(input("Enter your Account Number: "))
        except ValueError:
            print("❌ Invalid account number format.")
            continue

        result = verify_password(acc_no)
        if result is None:
            if input("🔁 Do you want to try again? (y/n): ").lower() != 'y':
                return
        elif result:
            cursor.execute("SELECT balance FROM accounts WHERE acc_no = %s", (acc_no,))
            result = cursor.fetchone()
            print(f"💰 Current Balance: ₹{result[0]}")
            return
        else:
            return


def deposit():
    while True:
        try:
            acc_no = int(input("Enter your Account Number: "))
        except ValueError:
            print("❌ Invalid account number format.")
            continue

        result = verify_password(acc_no)
        if result is None:
            if input("🔁 Do you want to try again? (y/n): ").lower() != 'y':
                return
        elif result:
            amount = float(input("Enter amount to deposit: "))
            cursor.execute("UPDATE accounts SET balance = balance + %s WHERE acc_no = %s", (amount, acc_no))
            db.commit()
            print("✅ Amount deposited successfully.")
            return
        else:
            return



def withdraw():
    while True:
        try:
            acc_no = int(input("Enter your Account Number: "))
        except ValueError:
            print("❌ Invalid account number format.")
            continue

        result = verify_password(acc_no)
        if result is None:
            if input("🔁 Do you want to try again? (y/n): ").lower() != 'y':
                return
        elif result:
            amount = float(input("Enter amount to withdraw: "))
            cursor.execute("SELECT balance FROM accounts WHERE acc_no = %s", (acc_no,))
            result = cursor.fetchone()
            if result and result[0] >= amount:
                cursor.execute("UPDATE accounts SET balance = balance - %s WHERE acc_no = %s", (amount, acc_no))
                db.commit()
                print("✅ Withdrawal successful.")
            else:
                print("❌ Insufficient balance.")
            return
        else:
            return








if __name__ == "__main__":
    while True:
        print("\n🏦 Bank Menu")
        print("1. Create Account")
        print("2. Check Balance")
        print("3. Deposit")
        print("4. Withdraw")
        print("5. Exit")

        choice = input("Select an option: ")

        match choice:
            case '1':
                create_account()
            case '2':
                check_balance()
            case '3':
                deposit()
            case '4':
                withdraw()
            case '5':
                print("Thank you for using the Bank App!")
                time.sleep(10)  # <-- Pause 10 seconds
            case _:
                print("❗ Invalid option")
