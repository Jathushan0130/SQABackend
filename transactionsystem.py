from read import read_old_bank_accounts
from write import write_new_current_accounts
from print_error import log_constraint_error
from authsystem import login
from transactionlogger import TransactionLogger

FILE_PATH = "currentaccounts.txt"

class TransactionSystem:
    def __init__(self):
        self.session_withdraw_total = 0.0
        self.session_transfer_total = 0.0
        self.session_bill_total = 0.0
        self.logger = TransactionLogger() 

    def log_transaction(self, transaction_type, description):
        print(f"SUCCESS: {transaction_type}: {description}")

    def interactive_withdraw(self) -> bool:
        """
        Withdraw money from an account.
          - Prompts for account holder’s name and account number.
          - Uses login() to verify the account.
          - Prompts for withdrawal amount.
          - For basic accounts, cumulative withdrawals in the session cannot exceed $500.
          - Ensures the account balance does not fall below $0.
        """
        print("=== Withdraw Money ===")
        admin_input = input("Are you logged in as admin? (y/n): ").strip().lower()
        holder_name = (input("Enter the account holder's name: ").strip() 
                       if admin_input == 'y' else input("Enter your name: ").strip())
        account_number = input("Enter the account number: ").strip()
        matching_account = login(account_number, holder_name, active_required=True)
        if matching_account is None:
            return False

        amount_str = input("Enter the amount to withdraw: ").strip()
        try:
            amount = float(amount_str)
        except ValueError:
            log_constraint_error("Withdraw", "Invalid amount entered")
            return False

        if matching_account.get("account_type", "basic") == "basic":
            if self.session_withdraw_total + amount > 500.00:
                log_constraint_error("Withdraw", "Exceeds maximum withdrawal limit for this session ($500.00)")
                return False

        if matching_account["balance"] < amount:
            log_constraint_error("Withdraw", "Insufficient funds in account")
            return False

        matching_account["balance"] -= amount
        # Re-read full accounts list and update the balance for persistence.
        accounts = read_old_bank_accounts(FILE_PATH)
        normalized = account_number.lstrip('0') or '0'
        for acc in accounts:
            if acc["account_number"] == normalized:
                acc["balance"] = matching_account["balance"]
                break
        write_new_current_accounts(accounts, FILE_PATH)
        self.session_withdraw_total += amount
        self.log_transaction("Withdraw", f"{amount} withdrawn from account {account_number}")
        # Log the transaction with code "01" and misc "WD"
        self.logger.log_transaction("01", holder_name, account_number, amount, "SP")
        return True

    def interactive_transfer(self) -> bool:
        """
        Transfer money between two accounts.
          - Prompts for the source account holder’s name and account number.
          - Uses login() to verify the source account.
          - Prompts for the destination account number and verifies that it exists.
          - For basic accounts, cumulative transfers in the session cannot exceed $1000.
          - Checks that the source account has sufficient funds.
        """
        print("=== Transfer Money ===")
        admin_input = input("Are you logged in as admin? (y/n): ").strip().lower()
        holder_name = (input("Enter the account holder's name (for the source account): ").strip()
                       if admin_input == 'y' else input("Enter your name: ").strip())
        from_account = input("Enter the source account number: ").strip()
        source_account = login(from_account, holder_name, active_required=True)
        if source_account is None:
            return False

        to_account = input("Enter the destination account number: ").strip()
        accounts = read_old_bank_accounts(FILE_PATH)
        dest_account = None
        for acc in accounts:
            if acc["account_number"] == to_account:
                dest_account = acc
                break
        if dest_account is None:
            log_constraint_error("Transfer", "Destination account not found")
            return False

        amount_str = input("Enter the amount to transfer: ").strip()
        try:
            amount = float(amount_str)
        except ValueError:
            log_constraint_error("Transfer", "Invalid amount entered")
            return False

        if source_account.get("account_type", "basic") == "basic":
            if self.session_transfer_total + amount > 1000.00:
                log_constraint_error("Transfer", "Exceeds maximum transfer limit for this session ($1000.00)")
                return False

        if source_account["balance"] < amount:
            log_constraint_error("Transfer", "Insufficient funds in source account")
            return False

        source_account["balance"] -= amount
        dest_account["balance"] += amount
        write_new_current_accounts(accounts, FILE_PATH)
        self.session_transfer_total += amount
        self.log_transaction("Transfer", f"{amount} transferred from account {from_account} to account {to_account}")
        # Log the transaction with code "02" and misc "TR"
        self.logger.log_transaction("02", holder_name, from_account, amount, "SP")
        return True

    def interactive_pay_bill(self) -> bool:
        """
        Pay a bill from an account.
          - Prompts for account holder’s name and account number.
          - Uses login() to verify the account.
          - Prompts for the company (must be one of the allowed companies) and the bill amount.
          - For basic accounts, cumulative bill payments in the session cannot exceed $2000.
          - Checks that the account has sufficient funds.
        """
        print("=== Pay Bill ===")
        admin_input = input("Are you logged in as admin? (y/n): ").strip().lower()
        holder_name = (input("Enter the account holder's name: ").strip()
                       if admin_input == 'y' else input("Enter your name: ").strip())
        account_number = input("Enter the account number: ").strip()
        matching_account = login(account_number, holder_name, active_required=True)
        if matching_account is None:
            return False

        company = input("Enter the company to whom the bill is being paid: ").strip()
        allowed_companies = {
            "The Bright Light Electric Company (EC)",
            "Credit Card Company Q (CQ)",
            "Fast Internet, Inc. (FI)"
        }
        if company not in allowed_companies:
            log_constraint_error("Pay Bill", f"Invalid company. Allowed companies: {', '.join(allowed_companies)}")
            return False

        amount_str = input("Enter the amount to pay: ").strip()
        try:
            amount = float(amount_str)
        except ValueError:
            log_constraint_error("Pay Bill", "Invalid amount entered")
            return False

        if matching_account.get("account_type", "basic") == "basic":
            if self.session_bill_total + amount > 2000.00:
                log_constraint_error("Pay Bill", "Exceeds maximum bill payment limit for this session ($2000.00)")
                return False

        if matching_account["balance"] < amount:
            log_constraint_error("Pay Bill", "Insufficient funds in account")
            return False

        matching_account["balance"] -= amount
        accounts = read_old_bank_accounts(FILE_PATH)
        normalized = account_number.lstrip('0') or '0'
        for acc in accounts:
            if acc["account_number"] == normalized:
                acc["balance"] = matching_account["balance"]
                break
        write_new_current_accounts(accounts, FILE_PATH)
        self.session_bill_total += amount
        self.log_transaction("Pay Bill", f"Paid {amount} to {company} from account {account_number}")
        # Log with code "03" and misc "PB"
        self.logger.log_transaction("03", holder_name, account_number, amount, "SP")
        return True

    def interactive_deposit(self) -> bool:
        """
        Deposit money into an account.
          - Prompts for account holder’s name and account number.
          - Uses login() to verify the account.
          - Prompts for the deposit amount.
          - Records the deposit transaction without making the funds available in the current session.
        """
        print("=== Deposit Money ===")
        admin_input = input("Are you logged in as admin? (y/n): ").strip().lower()
        holder_name = (input("Enter the account holder's name: ").strip()
                       if admin_input == 'y' else input("Enter your name: ").strip())
        account_number = input("Enter the account number: ").strip()
        matching_account = login(account_number, holder_name, active_required=True)
        if matching_account is None:
            return False

        amount_str = input("Enter the amount to deposit: ").strip()
        try:
            amount = float(amount_str)
        except ValueError:
            log_constraint_error("Deposit", "Invalid amount entered")
            return False

        self.log_transaction("Deposit", f"Recorded deposit of {amount} to account {account_number}. Funds will be available next session.")
        # Log with code "04" and misc "DP"
        self.logger.log_transaction("04", holder_name, account_number, amount, "SP")
        return True

    def interactive_change_plan(self) -> bool:
        """
        Change the transaction payment plan for an account.
          - Prompts for account holder’s name and account number.
          - Uses login() to verify the account.
          - Only allowed if the account is on a student plan (SP) and the user is an admin.
          - Changes the account’s payment plan from student (SP) to non-student (NP).
        """
        print("=== Change Transaction Payment Plan ===")
        if input("Are you logged in as admin? (y/n): ").strip().lower() != 'y':
            log_constraint_error("Change Plan", "Change plan transaction requires admin privileges")
            return False

        holder_name = input("Enter the account holder's name: ").strip()
        account_number = input("Enter the account number: ").strip()
        matching_account = login(account_number, holder_name, active_required=True)
        if matching_account is None:
            return False

        if matching_account.get("account_type") != "SP":
            log_constraint_error("Change Plan", "Account is not on a student plan (SP)")
            return False

        matching_account["account_type"] = "NP"
        accounts = read_old_bank_accounts(FILE_PATH)
        normalized = account_number.lstrip('0') or '0'
        for acc in accounts:
            if acc["account_number"] == normalized:
                acc["account_type"] = "NP"
                break
        write_new_current_accounts(accounts, FILE_PATH)
        self.log_transaction("Change Plan", f"Account {account_number} payment plan changed to non-student (NP)")
        # Log with code "08" and misc "CP"
        self.logger.log_transaction("08", holder_name, account_number, 0.0, "NP")
        return True
