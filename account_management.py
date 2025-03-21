from read import read_old_bank_accounts
from write import write_new_current_accounts
from print_error import log_constraint_error

def create_account(account_number: str, name: str, balance: float) -> bool:
    """Creates a new admin or standard account interactively."""
    accounts = read_old_bank_accounts("currentaccounts.txt")  # Load existing accounts

    # Ask user for account type
    account_type_input = input("Enter account type (admin / standard): ").strip().lower()
    if account_type_input == "admin":
        account_type = "admin"
    elif account_type_input == "standard":
        account_type = "basic"
    else:
        log_constraint_error("Account Creation", f"Invalid account type: {account_type_input}")
        return False

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
    
    return None 
