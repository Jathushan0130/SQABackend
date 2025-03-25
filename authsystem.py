from transactionlogger import TransactionLogger
from typing import Optional

def login(account_number: str, name: str, active_required: bool = True) -> Optional[dict]:
    # (Existing code – unchanged)
    from read import read_old_bank_accounts
    from print_error import log_constraint_error
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
    from read import read_old_bank_accounts
    normalized = account_number.lstrip('0') or '0'
    accounts = read_old_bank_accounts("currentaccounts.txt")
    for acc in accounts:
        if acc["account_number"] == normalized:
            if normalized == "1" and acc.get("name") == "Admin":
                return True
    return False

def logout() -> None:
    # Finalize the transaction log file (simulate download)
    logger = TransactionLogger()
    logger.end_session()
