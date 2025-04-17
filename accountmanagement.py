from read import read_old_bank_accounts
from typing import Optional, Tuple
from write import write_new_current_accounts
from print_error import log_constraint_error
from authsystem import login, is_admin
from transactionlogger import TransactionLogger

FILE_PATH = "currentaccounts.txt"

class AccountManager:
    def __init__(self):
        self.new_accounts = set()
        self.logger = TransactionLogger()

    def log_transaction(self, transaction_type, description):
        print(f"SUCCESS: {transaction_type}: {description}")

    def get_admin_credentials(self) -> Optional[Tuple[str, str]]:
        admin_acc = input("Enter your admin account number: ").strip()
        admin_name = input("Enter your admin account name: ").strip()
        admin_user = login(admin_acc, admin_name, active_required=True)
        if admin_user is None or not is_admin(admin_acc):
            log_constraint_error("Admin Authentication", "Invalid admin credentials or account is not an admin.")
            return None
        return admin_acc, admin_name
    
    def increment_transaction_counter(self, account_number: str, accounts: list) -> None:
        for acc in accounts:
            if acc['account_number'] == account_number:
                acc['total_transactions'] += 1
                break

    def create_sample_account(self) -> bool:
        accounts = read_old_bank_accounts(FILE_PATH)
        created = False

        # ensure sample Admin exists
        if not any(acc["account_number"] == "1" for acc in accounts):
            sample_admin = {
                "account_number": "00001",
                "name":           "Admin",
                "balance":        10000.00,
                "account_type":   "admin",
                "status":         "A",
                "total_transactions": 0
            }
            accounts.append(sample_admin)
            self.new_accounts.add("00001")
            self.log_transaction("Create Account",
                                 "Sample admin account (00001) created for Admin with balance 10000.00")
            self.logger.log_transaction("05", "Admin", "00001", 10000.00, "SP")
            self.increment_transaction_counter("00001", accounts)
            created = True

        # ensure sample Standard exists
        if not any(acc["account_number"] == "2" for acc in accounts):
            sample_standard = {
                "account_number":      "00002",
                "name":                "Standard",
                "balance":             5000.00,
                "account_type":        "basic",
                "status":              "A",
                "total_transactions":  0
            }
            accounts.append(sample_standard)
            self.new_accounts.add("00002")
            self.log_transaction("Create Account",
                                 "Sample standard account (00002) created for Standard with balance 5000.00")
            self.logger.log_transaction("05", "Standard", "00002", 5000.00, "SP")
            self.increment_transaction_counter("00002", accounts)
            created = True

        if created:
            write_new_current_accounts(accounts, FILE_PATH)
        else:
            print("Sample accounts already exist.")
            return True

        accounts_after = read_old_bank_accounts(FILE_PATH)
        print("Accounts after sample account creation:")
        for acc in accounts_after:
            print(acc)
        return True

    def create_account(self) -> bool:
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
            "status": "A",
            "total_transactions": 0
        }
        accounts.append(new_account)
        write_new_current_accounts(accounts, FILE_PATH)
        self.new_accounts.add(account_number)
        self.log_transaction("Create Account", f"Account {account_number} ({acc_type}) created for {name} with balance {balance}.")
        self.logger.log_transaction("05", name, account_number, balance, "SP")
        self.increment_transaction_counter(account_number, accounts)
        write_new_current_accounts(accounts, FILE_PATH)
        print("Note: This account will not be available for transactions until the next session.")
        return True

    def delete_account(self) -> bool:
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
        self.logger.log_transaction("06", target_name, target_account_number, 0.0, "SP")
        self.increment_transaction_counter(target_account_number, accounts)
        write_new_current_accounts(updated_accounts, FILE_PATH)
        return True

    def disable_account(self) -> bool:
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

        self.increment_transaction_counter(target_account_number, accounts)
        write_new_current_accounts(accounts, FILE_PATH)
        self.log_transaction("Disable Account", f"Account {target_account_number} for {target_name} disabled.")
        self.logger.log_transaction("07", target_name, target_account_number, 0.0, "SP")
        return True
