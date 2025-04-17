from accountmanagement import AccountManager
from transactionsystem import TransactionSystem
from authsystem import login, is_admin
from read import read_old_bank_accounts
from transactionlogger import TransactionLogger

FILE_PATH = "currentaccounts.txt"

def clear_data():
    open(FILE_PATH, 'w').close()

def welcome():
    print("=" * 40)
    print("     Welcome to SimpleBank CLI")
    print("=" * 40)
    print("Please log in. You can choose Admin or Standard.")
    print("Default Admin:    number=00001, name=Admin")
    print("Default Standard: number=00002, name=Standard\n")

def prompt_login():
    # first choose role
    while True:
        role = input("Login as (admin/standard)? ").strip().lower()
        if role in ("admin", "standard"):
            break
        print("Please enter 'admin' or 'standard'.")
    # then prompt credentials
    while True:
        acc_num = input("Account Number: ").strip()
        name    = input("Account Name  : ").strip()
        user = login(acc_num, name, active_required=True)
        if user and (role == "standard" or is_admin(acc_num)):
            print(f"\n✔ Logged in as {name} ({role.capitalize()})\n")
            return user
        print("❌ Login failed or insufficient privileges. Try again.\n")

def print_menu(is_admin_user):
    print("Select an operation:")
    menu_items = [
        ("1", "Create New Account",      True),
        ("2", "Delete Existing Account", True),
        ("3", "Disable Account",         True),
        ("4", "Withdraw Money",          False),
        ("5", "Deposit Money",           False),
        ("6", "Transfer Money",          False),
        ("7", "Pay Bill",                False),
        ("8", "Change Payment Plan",     True),
        ("9", "View All Accounts",       False),
        ("0", "Exit",                    False),
    ]
    for code, label, admin_only in menu_items:
        if not admin_only or is_admin_user:
            print(f"  {code}. {label}")
    return input("Enter choice: ").strip()

def main():
    clear_data()

    # Create built-in sample accounts before login
    am = AccountManager()
    am.create_sample_account()

    welcome()
    user = prompt_login()
    admin_flag = is_admin(user['account_number'])
    ts = TransactionSystem()

    while True:
        choice = print_menu(admin_flag)
        print()
        if choice == "1" and admin_flag:
            am.create_account()
        elif choice == "2" and admin_flag:
            am.delete_account()
        elif choice == "3" and admin_flag:
            am.disable_account()
        elif choice == "4":
            ts.interactive_withdraw()
        elif choice == "5":
            ts.interactive_deposit()
        elif choice == "6":
            ts.interactive_transfer()
        elif choice == "7":
            ts.interactive_pay_bill()
        elif choice == "8" and admin_flag:
            ts.interactive_change_plan()
        elif choice == "9":
            print("\nCurrent Accounts:")
            for acc in read_old_bank_accounts(FILE_PATH):
                print(acc)
        elif choice == "0":
            break
        else:
            print("⚠ Invalid choice or insufficient privileges.\n")

    # Final summary
    print("\n--- Final Account List ---")
    for acc in read_old_bank_accounts(FILE_PATH):
        print(acc)
    print("\n--- Ending Session ---")
    TransactionLogger().end_session()

if __name__ == "__main__":
    main()
