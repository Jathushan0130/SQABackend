from accountmanagement import AccountManager
from transactionsystem import TransactionSystem
from read import read_old_bank_accounts
from transactionlogger import TransactionLogger

FILE_PATH = "currentaccounts.txt"

def main():
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
    input_backup = __builtins__.input
    __builtins__.input = lambda _: next(input_sequence)
    am.create_account()
    __builtins__.input = input_backup

    # Create a standard account that will later be disabled.
    print("\n--- TEST: Create Standard Account for Disabled Test (DisabledUser) ---")
    input_sequence = iter([
        'y', '00001', 'Admin',
        'DisabledUser', '10002', 'basic', '2000.00'
    ])
    __builtins__.input = lambda _: next(input_sequence)
    am.create_account()
    __builtins__.input = input_backup

    # Disable the account for testing disabled behavior.
    print("\n--- TEST: Disable Standard Account (DisabledUser) ---")
    input_sequence = iter([
        'y', '00001', 'Admin',
        'DisabledUser', '10002'
    ])
    __builtins__.input = lambda _: next(input_sequence)
    am.disable_account()
    __builtins__.input = input_backup

    # Create extra accounts for deposit, transfer, and delete tests
    print("\n--- TEST: Create TransferUser and DeleteUser ---")
    input_sequence = iter([
        'y', '00001', 'Admin', 'TransferUser', '10003', 'basic', '1000.00',
        'y', '00001', 'Admin', 'DeleteUser', '10004', 'basic', '800.00'
    ])
    __builtins__.input = lambda _: next(input_sequence)
    am.create_account()
    am.create_account()
    __builtins__.input = input_backup

    # Deposit into ActiveUser
    print("\n--- TEST: Deposit ---")
    input_sequence = iter(['n', 'ActiveUser', '10001', '300'])
    __builtins__.input = lambda _: next(input_sequence)
    ts.interactive_deposit()
    __builtins__.input = input_backup

    # Transfer from ActiveUser to TransferUser
    print("\n--- TEST: Transfer ---")
    input_sequence = iter(['n', 'ActiveUser', '10001', '10003', '200'])
    __builtins__.input = lambda _: next(input_sequence)
    ts.interactive_transfer()
    __builtins__.input = input_backup

    # Pay bill from ActiveUser
    print("\n--- TEST: Pay Bill ---")
    input_sequence = iter(['n', 'ActiveUser', '10001', 'Fast Internet, Inc. (FI)', '100'])
    __builtins__.input = lambda _: next(input_sequence)
    ts.interactive_pay_bill()
    __builtins__.input = input_backup

    # Change plan (will fail if not SP)
    print("\n--- TEST: Change Plan ---")
    input_sequence = iter(['y', 'ActiveUser', '10001'])
    __builtins__.input = lambda _: next(input_sequence)
    ts.interactive_change_plan()
    __builtins__.input = input_backup

    # Delete DeleteUser account
    print("\n--- TEST: Delete Account ---")
    input_sequence = iter(['y', '00001', 'Admin', 'DeleteUser', '10004'])
    __builtins__.input = lambda _: next(input_sequence)
    am.delete_account()
    __builtins__.input = input_backup

    # View all accounts
    print("\n--- Final Account List ---")
    final_accounts = read_old_bank_accounts(FILE_PATH)
    for acc in final_accounts:
        print(acc)

    # End the session and log the transaction log end-of-session marker.
    print("\n--- Ending Session: Logging Transactions ---")
    logger = TransactionLogger()
    logger.end_session()

if __name__ == "__main__":
    main()
