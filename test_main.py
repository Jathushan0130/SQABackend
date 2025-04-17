from accountmanagement import AccountManager
from transactionsystem import TransactionSystem
from read import read_old_bank_accounts
from transactionlogger import TransactionLogger

FILE_PATH = "currentaccounts.txt"

def main():
    # Clear out any existing accounts file so tests start fresh
    open(FILE_PATH, 'w').close()

    am = AccountManager()
    ts = TransactionSystem()

    # Create sample admin account.
    print("\n--- Creating Sample Admin Account ---")
    am.create_sample_account()

    # Create an active standard account.
    print("\n--- TEST: Create Active Standard Account (ActiveUser) ---")
    input_sequence = iter([
        'y', '00001', 'Admin',
        'ActiveUser', '10001', 'basic', '1500.00'
    ])
    backup = __builtins__.input
    __builtins__.input = lambda _: next(input_sequence)
    am.create_account()
    __builtins__.input = backup

    # Create a standard account that will later be disabled.
    print("\n--- TEST: Create Standard Account for Disabled Test (DisabledUser) ---")
    input_sequence = iter([
        'y', '00001', 'Admin',
        'DisabledUser', '10002', 'basic', '2000.00'
    ])
    __builtins__.input = lambda _: next(input_sequence)
    am.create_account()
    __builtins__.input = backup

    # Disable the account for testing disabled behavior.
    print("\n--- TEST: Disable Standard Account (DisabledUser) ---")
    input_sequence = iter([
        'y', '00001', 'Admin',
        'DisabledUser', '10002'
    ])
    __builtins__.input = lambda _: next(input_sequence)
    am.disable_account()
    __builtins__.input = backup

    # Create extra accounts for deposit, transfer, and delete tests
    print("\n--- TEST: Create TransferUser and DeleteUser ---")
    input_sequence = iter([
        'y', '00001', 'Admin', 'TransferUser', '10003', 'basic', '1000.00',
        'y', '00001', 'Admin', 'DeleteUser',   '10004', 'basic', ' 800.00'
    ])
    __builtins__.input = lambda _: next(input_sequence)
    am.create_account()
    am.create_account()
    __builtins__.input = backup

    # Deposit into ActiveUser
    print("\n--- TEST: Deposit ---")
    input_sequence = iter(['n', 'ActiveUser', '10001', '300'])
    __builtins__.input = lambda _: next(input_sequence)
    ts.interactive_deposit()
    __builtins__.input = backup

    # Transfer from ActiveUser to TransferUser
    print("\n--- TEST: Transfer ---")
    input_sequence = iter(['n', 'ActiveUser', '10001', '10003', '200'])
    __builtins__.input = lambda _: next(input_sequence)
    ts.interactive_transfer()
    __builtins__.input = backup

    # Pay bill from ActiveUser
    print("\n--- TEST: Pay Bill ---")
    input_sequence = iter(['n', 'ActiveUser', '10001', 'Fast Internet, Inc. (FI)', '100'])
    __builtins__.input = lambda _: next(input_sequence)
    ts.interactive_pay_bill()
    __builtins__.input = backup

    # Change plan (will fail if not SP)
    print("\n--- TEST: Change Plan ---")
    input_sequence = iter(['y', 'ActiveUser', '10001'])
    __builtins__.input = lambda _: next(input_sequence)
    ts.interactive_change_plan()
    __builtins__.input = backup

    # Delete DeleteUser account
    print("\n--- TEST: Delete Account ---")
    input_sequence = iter(['y', '00001', 'Admin', 'DeleteUser', '10004'])
    __builtins__.input = lambda _: next(input_sequence)
    am.delete_account()
    __builtins__.input = backup

    # Standard‐account threshold tests (all should fail):

    print("\n--- TEST: Standard Withdraw Exceeds $500 (Should Fail) ---")
    # session_withdraw_total is already 500 from earlier withdraw test
    input_sequence = iter(['n', 'ActiveUser', '10001', '1'])
    __builtins__.input = lambda _: next(input_sequence)
    ts.interactive_withdraw()
    __builtins__.input = backup

    print("\n--- TEST: Standard Transfer Exceeds $1000 (Should Fail) ---")
    # session_transfer_total is already 200
    input_sequence = iter(['n', 'ActiveUser', '10001', '10003', '900'])
    __builtins__.input = lambda _: next(input_sequence)
    ts.interactive_transfer()
    __builtins__.input = backup

    print("\n--- TEST: Standard Pay Bill Exceeds $2000 (Should Fail) ---")
    # session_bill_total is already 100
    input_sequence = iter(['n', 'ActiveUser', '10001', 'Fast Internet, Inc. (FI)', '2000'])
    __builtins__.input = lambda _: next(input_sequence)
    ts.interactive_pay_bill()
    __builtins__.input = backup

    # Admin‐account threshold bypass tests (all should succeed):

    print("\n--- TEST: Admin Withdraw 600 (Bypass $500 Limit) ---")
    input_sequence = iter(['y', 'Admin', '00001', '600'])
    __builtins__.input = lambda _: next(input_sequence)
    ts.interactive_withdraw()
    __builtins__.input = backup

    print("\n--- TEST: Admin Transfer 1500 (Bypass $1000 Limit) ---")
    input_sequence = iter(['y', 'Admin', '00001', '10001', '1500'])
    __builtins__.input = lambda _: next(input_sequence)
    ts.interactive_transfer()
    __builtins__.input = backup

    print("\n--- TEST: Admin Pay Bill 2500 (Bypass $2000 Limit) ---")
    input_sequence = iter(['y', 'Admin', '00001', 'Fast Internet, Inc. (FI)', '2500'])
    __builtins__.input = lambda _: next(input_sequence)
    ts.interactive_pay_bill()
    __builtins__.input = backup

    # View all accounts
    print("\n--- Final Account List ---")
    for acc in read_old_bank_accounts(FILE_PATH):
        print(acc)

    # End the session and log the transaction log end-of-session marker.
    print("\n--- Ending Session: Logging Transactions ---")
    TransactionLogger().end_session()

if __name__ == "__main__":
    main()
