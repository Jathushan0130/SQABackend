from read import read_old_bank_accounts
from write import write_new_current_accounts
from print_error import log_constraint_error
from auth_system import is_admin

def create_account(admin_account_number: str, account_number: str, name: str, balance: float, account_type: str) -> bool:
    """Creates a new account if admin is authorized."""
    if not is_admin(admin_account_number):
        log_constraint_error("Account Creation", f"Unauthorized access by {admin_account_number}")
        return False

    accounts = read_old_bank_accounts("currentaccounts.txt")

    if any(acc["account_number"] == account_number for acc in accounts):
        log_constraint_error("Account Creation", f"Account {account_number} already exists")
        return False

    new_account = {
        "account_number": account_number,
        "name": name,
        "balance": balance,
        "account_type": account_type,
        "status": "A",
        "total_transactions": 0
    }

    accounts.append(new_account)
    write_new_current_accounts(accounts, "currentaccounts.txt")
    return True


def delete_account(admin_account_number: str, account_number: str) -> bool:
    """Deletes an account if admin is authorized."""
    if not is_admin(admin_account_number):
        log_constraint_error("Account Deletion", f"Unauthorized access by {admin_account_number}")
        return False

    accounts = read_old_bank_accounts("currentaccounts.txt")
    updated_accounts = [acc for acc in accounts if acc["account_number"] != account_number]

    if len(updated_accounts) == len(accounts):
        log_constraint_error("Account Deletion", f"Account {account_number} not found")
        return False

    write_new_current_accounts(updated_accounts, "currentaccounts.txt")
    return True


def update_account(admin_account_number: str, account_number: str, field: str, new_value: any) -> bool:
    """Updates an account field if admin is authorized."""
    if not is_admin(admin_account_number):
        log_constraint_error("Account Update", f"Unauthorized access by {admin_account_number}")
        return False

    accounts = read_old_bank_accounts("currentaccounts.txt")

    for acc in accounts:
        if acc["account_number"] == account_number:
            if field not in acc:
                log_constraint_error("Account Update", f"Field {field} not found")
                return False

            acc[field] = new_value
            write_new_current_accounts(accounts, "currentaccounts.txt")
            return True

    log_constraint_error("Account Update", f"Account {account_number} not found")
    return False


def get_account(admin_account_number: str, account_number: str) -> dict | None:
    """Retrieves an account’s details if admin is authorized."""
    if not is_admin(admin_account_number):
        log_constraint_error("Get Account", f"Unauthorized access by {admin_account_number}")
        return None

    accounts = read_old_bank_accounts("currentaccounts.txt")

    for acc in accounts:
        if acc["account_number"] == account_number:
            return acc

    return None


def disable_account(admin_account_number: str, account_number: str) -> bool:
    """Disables an account if admin is authorized."""
    if not is_admin(admin_account_number):
        log_constraint_error("Account Disable", f"Unauthorized access by {admin_account_number}")
        return False

    accounts = read_old_bank_accounts("currentaccounts.txt")

    for acc in accounts:
        if acc["account_number"] == account_number:
            if acc["status"] == "D":
                log_constraint_error("Account Disable", "Account already disabled")
                return False
            acc["status"] = "D"
            write_new_current_accounts(accounts, "currentaccounts.txt")
            return True

    log_constraint_error("Account Disable", "Account not found")
    return False
