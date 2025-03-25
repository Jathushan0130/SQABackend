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
        'y', '00001', 'Admin',   # Admin login for account creation.
        'ActiveUser', '10001', 'basic', '1500.00'
    ])
    input_backup = __builtins__.input
    __builtins__.input = lambda _: next(input_sequence)
    am.create_account()
    __builtins__.input = input_backup

    # Create a standard account that will later be disabled.
    print("\n--- TEST: Create Standard Account for Disabled Test (DisabledUser) ---")
    input_sequence = iter([
        'y', '00001', 'Admin',   # Admin login for account creation.
        'DisabledUser', '10002', 'basic', '2000.00'
    ])
    __builtins__.input = lambda _: next(input_sequence)
    am.create_account()
    __builtins__.input = input_backup

    # Disable the account for testing disabled behavior.
    print("\n--- TEST: Disable Standard Account (DisabledUser) ---")
    input_sequence = iter([
        'y', '00001', 'Admin',   # Admin login for disabling account.
        'DisabledUser', '10002'
    ])
    __builtins__.input = lambda _: next(input_sequence)
    am.disable_account()
    __builtins__.input = input_backup

    # Display all accounts after modifications.
    print("\n--- TEST: View Accounts After Admin Changes ---")
    accounts = read_old_bank_accounts(FILE_PATH)
    for acc in accounts:
        print(acc)

    # Test a transaction on the active standard account (should succeed).
    print("\n--- TEST: Withdraw with Active Standard Account (ActiveUser) ---")
    input_sequence = iter([
        'n', 'ActiveUser', '10001',  # ActiveUser is still active.
        '500'
    ])
    __builtins__.input = lambda _: next(input_sequence)
    ts.interactive_withdraw()
    __builtins__.input = input_backup

    # Test a transaction on the disabled account (should fail).
    print("\n--- TEST: Withdraw with Disabled Account (DisabledUser, Should Fail) ---")
    input_sequence = iter([
        'n', 'DisabledUser', '10002',  # DisabledUser is inactive; login should fail.
        '500'
    ])
    __builtins__.input = lambda _: next(input_sequence)
    ts.interactive_withdraw()
    __builtins__.input = input_backup

    # End the session and log the transaction log end-of-session marker.
    print("\n--- Ending Session: Logging Transactions ---")
    logger = TransactionLogger()
    logger.end_session()

    # Final account list.
    print("\n--- Final Account List ---")
    final_accounts = read_old_bank_accounts(FILE_PATH)
    for acc in final_accounts:
        print(acc)

if __name__ == "__main__":
    main()
