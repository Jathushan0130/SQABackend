from read import read_old_bank_accounts
from print_error import log_constraint_error

def login(account_number: str, name: str, active_required: bool = True) -> dict | None:
    # Normalize the account number by stripping leading zeros.
    normalized = account_number.lstrip('0') or '0'
    accounts = read_old_bank_accounts("currentaccounts.txt")
    for acc in accounts:
        if acc["account_number"] == normalized and acc["name"] == name:
            if active_required and acc["status"] != "A":
                log_constraint_error("Authentication", f"Account {account_number} is not active.")
                return None
            return acc
    log_constraint_error("Authentication", f"Account {account_number} not found or name mismatch.")
    return None

def is_admin(account_number: str) -> bool:
    """
    Since the file format doesn't store account_type, we'll assume that the
    sample admin account has normalized account number "1" and name "Admin".
    """
    normalized = account_number.lstrip('0') or '0'
    accounts = read_old_bank_accounts("currentaccounts.txt")
    for acc in accounts:
        if acc["account_number"] == normalized:
            # Check if this account is the sample admin account.
            if normalized == "1" and acc.get("name") == "Admin":
                return True
    return False

def logout() -> None:
    pass
