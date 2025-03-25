from read import read_old_bank_accounts
from write import write_new_current_accounts
from print_error import log_constraint_error

FILE_PATH = "currentaccounts.txt"

def increment_transaction_count(account_number: str) -> bool:
    normalized = account_number.lstrip('0') or '0'
    accounts = read_old_bank_accounts(FILE_PATH)
    updated = False

    for acc in accounts:
        if acc["account_number"] == normalized:
            acc["total_transactions"] = acc.get("total_transactions", 0) + 1
            updated = True
            break

    if not updated:
        log_constraint_error("Transaction Counter", f"Account {account_number} not found.")
        return False

    try:
        write_new_current_accounts(accounts, FILE_PATH)
    except Exception as e:
        log_constraint_error("Transaction Counter", f"Failed to update total transactions: {e}")
        return False

    return True
