from read import read_old_bank_accounts
from write import write_new_current_accounts
from print_error import log_constraint_error

def create_account(account_number: str, name: str, balance: float, account_type: str) -> bool:
    """Creates a new account if it doesn't already exist."""
    accounts = read_old_bank_accounts("currentaccounts.txt")  # Load existing accounts

    if any(acc["account_number"] == account_number for acc in accounts):
        log_constraint_error("Account Creation", f"Account {account_number} already exists")
        return False  # Account already exists
    
    new_account = {
        "account_number": account_number,
        "name": name,
        "balance": balance,
        "account_type": account_type,
        "status": "A"
    }

    accounts.append(new_account)  # Add new account
    write_new_current_accounts(accounts, "currentaccounts.txt")  # Save updated accounts
    return True  # Success


def delete_account(account_number: str) -> bool:
    """Deletes an account if it exists."""
    accounts = read_old_bank_accounts("currentaccounts.txt")
    
    updated_accounts = [acc for acc in accounts if acc["account_number"] != account_number]
    
    if len(updated_accounts) == len(accounts):
        log_constraint_error("Account Deletion", f"Account {account_number} not found")
        return False  # Account not found
    
    write_new_current_accounts(updated_accounts, "currentaccounts.txt")
    return True  # Success


def update_account(account_number: str, field: str, new_value: any) -> bool:
    """Updates an account's balance or type."""
    accounts = read_old_bank_accounts("currentaccounts.txt")
    
    for acc in accounts:
        if acc["account_number"] == account_number:
            if field not in acc:
                log_constraint_error("Account Update", f"Field {field} not found")
                return False  # Invalid field
            
            acc[field] = new_value
            write_new_current_accounts(accounts, "currentaccounts.txt")
            return True  # Success
    
    log_constraint_error("Account Update", f"Account {account_number} not found")
    return False  # Account not found


def get_account(account_number: str) -> dict | None:
    """Retrieves an account’s details."""
    accounts = read_old_bank_accounts("currentaccounts.txt")
    
    for acc in accounts:
        if acc["account_number"] == account_number:
            return acc
    
    return None  # Account not found


def disable_account(account_number: str) -> bool:
    """Disables an account by setting its status to 'D'."""
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
