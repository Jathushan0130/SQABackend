from read import read_old_bank_accounts
from write import write_new_current_accounts
from print_error import log_constraint_error
from authsystem import login, is_admin

FILE_PATH = "currentaccounts.txt"

class AccountManager:
    def __init__(self):
        # Tracks newly created accounts in this session.
        self.new_accounts = set()
    
    def log_transaction(self, transaction_type, description):
        print(f"SUCCESS: {transaction_type}: {description}")
    
    def get_admin_credentials(self) -> tuple[str, str] | None:
        """
        Prompts for admin credentials and verifies them using login() and is_admin().
        Returns a tuple (admin_account_number, admin_name) if successful; otherwise returns None.
        """
        admin_acc = input("Enter your admin account number: ").strip()
        admin_name = input("Enter your admin account name: ").strip()
        admin_user = login(admin_acc, admin_name, active_required=True)
        if admin_user is None or not is_admin(admin_acc):
            log_constraint_error("Admin Authentication", "Invalid admin credentials or account is not an admin.")
            return None
        return admin_acc, admin_name

    def create_sample_account(self) -> bool:
        """
        Creates a sample admin account with account number '00001' and name 'Admin'
        if it does not already exist.
        """
        accounts = read_old_bank_accounts(FILE_PATH)
        # Because read_old_bank_accounts normalizes account numbers, "00001" will be read as "1".
        if any(acc["account_number"] == "1" for acc in accounts):
            print("Sample admin account already exists.")
            return True

        sample_account = {
            "account_number": "00001",  # Must be 5-digit string for write validation.
            "name": "Admin",
            "balance": 1000.00,
            "account_type": "admin",  # Not used in file formatting but useful for logic.
            "status": "A",            # Must be either "A" or "D".
            "total_transactions": 0
        }
        accounts.append(sample_account)
        try:
            write_new_current_accounts(accounts, FILE_PATH)
            self.new_accounts.add("00001")
            self.log_transaction("Create Account", "Sample admin account (00001) created for Admin with balance 1000.00")
        except Exception as e:
            print(f"Failed to write accounts file: {e}")
            return False

        # Read back the file to verify sample account is present.
        accounts_after = read_old_bank_accounts(FILE_PATH)
        print("Accounts after sample account creation:")
        for acc in accounts_after:
            print(acc)
        return True

    def create_account(self) -> bool:
        """
        Create a new bank account with an initial balance.
        
        Requirements:
          • Prompts for admin credentials.
          • Prompts for the account holder’s name (max 20 characters).
          • Prompts for a unique account number.
          • Prompts for the account type (admin/basic).
          • Prompts for the initial balance (at most $99999.99).
          • Privileged transaction (admin only).
          • The new account will not be available for other transactions in this session.
        """
        print("=== Create New Bank Account ===")
        if input("Are you logged in as admin? (y/n): ").strip().lower() != 'y':
            log_constraint_error("Create Account", "Account creation requires admin privileges.")
            return False

        if self.get_admin_credentials() is None:
            return False

        name = input("Enter the account holder's name (max 20 characters): ").strip()
        if len(name) > 20:
            log_constraint_error("Create Account", "Account holder's name exceeds 20 characters.")
            return False

        account_number = input("Enter the new account number: ").strip()
        accounts = read_old_bank_accounts(FILE_PATH)
        if any(acc["account_number"] == account_number for acc in accounts):
            log_constraint_error("Create Account", "Account number already exists.")
            return False

        # Prompt for account type
        acc_type = input("Enter account type (admin/basic): ").strip().lower()
        if acc_type not in ("admin", "basic"):
            log_constraint_error("Create Account", "Invalid account type. Must be 'admin' or 'basic'.")
            return False

        balance_str = input("Enter the initial balance (max $99999.99): ").strip()
        try:
            balance = float(balance_str)
        except ValueError:
            log_constraint_error("Create Account", "Invalid balance amount entered.")
            return False

        if balance > 99999.99:
            log_constraint_error("Create Account", "Initial balance exceeds $99999.99.")
            return False

        new_account = {
            "account_number": account_number,
            "name": name,
            "balance": balance,
            "account_type": acc_type,
            "status": "A",  # Must be "A" (active) or "D".
            "total_transactions": 0
        }
        accounts.append(new_account)
        write_new_current_accounts(accounts, FILE_PATH)
        self.new_accounts.add(account_number)
        self.log_transaction("Create Account", f"Account {account_number} ({acc_type}) created for {name} with balance {balance}.")
        print("Note: This account will not be available for transactions until the next session.")
        return True

    def delete_account(self) -> bool:
        """
        Delete a bank account.
        
        Requirements:
          • Prompts for admin credentials.
          • Prompts for the target account holder’s name and account number.
          • Verifies that the target account exists and that the provided name matches.
          • Privileged transaction (admin only).
          • Once deleted, no further transactions are accepted on that account.
        """
        print("=== Delete Bank Account ===")
        if input("Are you logged in as admin? (y/n): ").strip().lower() != 'y':
            log_constraint_error("Delete Account", "Deletion requires admin privileges.")
            return False

        if self.get_admin_credentials() is None:
            return False

        target_name = input("Enter the target account holder's name: ").strip()
        target_account_number = input("Enter the target account number: ").strip()
        accounts = read_old_bank_accounts(FILE_PATH)
        target_found = False
        for acc in accounts:
            if acc["account_number"] == target_account_number:
                if acc["name"] != target_name:
                    log_constraint_error("Delete Account", "Target account holder's name does not match.")
                    return False
                target_found = True
                break

        if not target_found:
            log_constraint_error("Delete Account", "Target account not found.")
            return False

        updated_accounts = [acc for acc in accounts if acc["account_number"] != target_account_number]
        write_new_current_accounts(updated_accounts, FILE_PATH)
        self.log_transaction("Delete Account", f"Account {target_account_number} for {target_name} deleted.")
        return True

    def disable_account(self) -> bool:
        """
        Disable a bank account.
        
        Requirements:
          • Prompts for admin credentials.
          • Prompts for the target account holder’s name and account number.
          • Verifies that the target account exists and that the provided name matches.
          • Changes the account status from active ("A") to disabled ("D").
          • Privileged transaction (admin only).
          • Once disabled, no further transactions are accepted on that account.
        """
        print("=== Disable Bank Account ===")
        if input("Are you logged in as admin? (y/n): ").strip().lower() != 'y':
            log_constraint_error("Disable Account", "Disabling an account requires admin privileges.")
            return False

        if self.get_admin_credentials() is None:
            return False

        target_name = input("Enter the target account holder's name: ").strip()
        target_account_number = input("Enter the target account number: ").strip()
        accounts = read_old_bank_accounts(FILE_PATH)
        target_found = False
        for acc in accounts:
            if acc["account_number"] == target_account_number:
                if acc["name"] != target_name:
                    log_constraint_error("Disable Account", "Target account holder's name does not match.")
                    return False
                if acc["status"] != "A":
                    log_constraint_error("Disable Account", "Account is not active and cannot be disabled.")
                    return False
                acc["status"] = "D"
                target_found = True
                break

        if not target_found:
            log_constraint_error("Disable Account", "Target account not found.")
            return False

        write_new_current_accounts(accounts, FILE_PATH)
        self.log_transaction("Disable Account", f"Account {target_account_number} for {target_name} disabled.")
        return True
