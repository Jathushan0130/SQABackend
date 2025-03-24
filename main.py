from accountmanagement import AccountManager
from transactionsystem import TransactionSystem
from read import read_old_bank_accounts

FILE_PATH = "currentaccounts.txt"

def main():
    am = AccountManager()
    ts = TransactionSystem()
    
    am.create_sample_account()
    
    print("=== Account Management ===")
    if am.create_account():
        print("Account creation succeeded.\n")
    else:
        print("Account creation failed.\n")
        
    if am.delete_account():
        print("Account deletion succeeded.\n")
    else:
        print("Account deletion failed.\n")
    
    if am.disable_account():
        print("Account disable succeeded.\n")
    else:
        print("Account disable failed.\n")
        
    print("=== Current Accounts ===")
    accounts = read_old_bank_accounts(FILE_PATH)
    for acc in accounts:
        print(acc)
        
    print("\n=== Transaction System ===")
    if ts.interactive_withdraw():
        print("Withdrawal succeeded.\n")
    else:
        print("Withdrawal failed.\n")
        
    if ts.interactive_transfer():
        print("Transfer succeeded.\n")
    else:
        print("Transfer failed.\n")
        
    if ts.interactive_pay_bill():
        print("Pay Bill succeeded.\n")
    else:
        print("Pay Bill failed.\n")
        
    if ts.interactive_deposit():
        print("Deposit recorded successfully.\n")
    else:
        print("Deposit failed.\n")
        
    if ts.interactive_change_plan():
        print("Change Plan succeeded.\n")
    else:
        print("Change Plan failed.\n")

if __name__ == "__main__":
    main()
