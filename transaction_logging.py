from read import read_old_bank_accounts
from write import write_new_current_accounts
from print_error import log_constraint_error

# ------------------------------------------------------------------------------
# 1) LOGGING SUCCESSFUL TRANSACTIONS
# ------------------------------------------------------------------------------

def log_transaction(transaction_type: str, description: str) -> None:
    """
    Logs a successful transaction to a file named 'transaction_logs.txt'.
    Example entry: "SUCCESS: Deposit: 100.00 to 12345"
    """
    log_filename = "transaction_logs.txt"
    with open(log_filename, "a") as log_file:
        log_file.write(f"SUCCESS: {transaction_type}: {description}\n")


# ------------------------------------------------------------------------------
# 2) READ TRANSACTIONS (NEW FUNCTION)
# ------------------------------------------------------------------------------

def read_transactions(filename: str) -> list:
    """
    Reads the transaction log file and returns a list of strings (each log line).
    """
    entries = []
    try:
        with open(filename, "r") as f:
            entries = f.readlines()
    except FileNotFoundError:
        # If no log file yet, just return an empty list
        pass

    # Strip trailing whitespace from each line
    return [line.strip() for line in entries]
