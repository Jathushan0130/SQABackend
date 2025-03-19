from read import read_old_bank_accounts
from print_error import log_constraint_error

def authenticate(account_number: str, name: str) -> bool:
    """
    Checks if an account already exists and matches it to the provided name.
    If the account is active and the name matches, it will return True.
    Otherwise, logs an error and returns False.
    """
    accounts = read_old_bank_accounts("currentaccounts.txt")
    for acc in accounts:
        # Check account number, name, and active status
        if acc["account_number"] == account_number and acc["name"] == name and acc["status"] == "A":
            return True
    
    # If no valid match, log error and return False
    log_constraint_error("Authentication", f"Failed login for account {account_number}")
    return False


def is_admin(account_number: str) -> bool:
    """
    Checks if an account is an admin.
    This example assumes there's a field "account_type" in each account,
    and an admin account will have "account_type" == "admin".
    """
    accounts = read_old_bank_accounts("currentaccounts.txt")
    for acc in accounts:
        if acc["account_number"] == account_number:
            # If 'account_type' exists, check if it equals 'admin'
            return acc.get("account_type") == "admin"
    return False


def logout() -> None:
    """
    Ends the session (if session tracking is needed).
    For now, this is a placeholder that does nothing.
    """
    pass
