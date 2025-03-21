from read import read_old_bank_accounts
from write import write_new_current_accounts
from print_error import log_constraint_error

# Placeholder logger for successful transactions
def log_transaction(transaction_type, description):
    print(f"SUCCESS: {transaction_type}: {description}")

FILE_PATH = "currentaccounts.txt"

# Deposit Function
def deposit(account_number: str, amount: float) -> bool:
    accounts = read_old_bank_accounts(FILE_PATH)
    for acc in accounts:
        if acc["account_number"] == account_number:
            if acc["status"] != "A":
                log_constraint_error("Deposit", f"Account {account_number} is not active")
                return False
            acc["balance"] += amount
            write_new_current_accounts(accounts, FILE_PATH)
            log_transaction("Deposit", f"{amount} to {account_number}")
            return True
    log_constraint_error("Deposit", f"Account {account_number} not found")
    return False

# Withdraw Function
def withdraw(account_number: str, amount: float) -> bool:
    accounts = read_old_bank_accounts(FILE_PATH)
    for acc in accounts:
        if acc["account_number"] == account_number:
            if acc["status"] != "A":
                log_constraint_error("Withdraw", f"Account {account_number} is not active")
                return False
            if acc["balance"] < amount:
                log_constraint_error("Withdraw", f"Insufficient funds in {account_number}")
                return False
            acc["balance"] -= amount
            write_new_current_accounts(accounts, FILE_PATH)
            log_transaction("Withdraw", f"{amount} from {account_number}")
            return True
    log_constraint_error("Withdraw", f"Account {account_number} not found")
    return False

# Transfer Function
def transfer(from_account: str, to_account: str, amount: float) -> bool:
    accounts = read_old_bank_accounts(FILE_PATH)
    from_acc = next((acc for acc in accounts if acc["account_number"] == from_account), None)
    to_acc = next((acc for acc in accounts if acc["account_number"] == to_account), None)

    if not from_acc or not to_acc:
        log_constraint_error("Transfer", f"Invalid accounts {from_account} or {to_account}")
        return False
    if from_acc["status"] != "A" or to_acc["status"] != "A":
        log_constraint_error("Transfer", "One or both accounts are inactive")
        return False
    if from_acc["balance"] < amount:
        log_constraint_error("Transfer", f"Insufficient funds in {from_account}")
        return False

    from_acc["balance"] -= amount
    to_acc["balance"] += amount
    write_new_current_accounts(accounts, FILE_PATH)
    log_transaction("Transfer", f"{amount} from {from_account} to {to_account}")
    return True

# Pay Bill Function
def pay_bill(account_number: str, bill_amount: float) -> bool:
    return withdraw(account_number, bill_amount)

# Change Plan Function
def change_plan(account_number: str, new_plan: str) -> bool:
    accounts = read_old_bank_accounts(FILE_PATH)
    for acc in accounts:
        if acc["account_number"] == account_number:
            acc["account_type"] = new_plan
            write_new_current_accounts(accounts, FILE_PATH)
            log_transaction("Change Plan", f"{account_number} plan changed to {new_plan}")
            return True
    log_constraint_error("Change Plan", f"Account {account_number} not found")
    return False

if __name__ == "__main__":
    from account_management import create_account

    print("\nCreating test accounts...")
    create_account("12345", "11111", "User One", 500.00, "basic")
    create_account("67890", "22222", "User Two", 300.00, "basic")

    print("Reading all accounts...")
    accounts = read_old_bank_accounts(FILE_PATH)
    for acc in accounts:
        print(acc)

    print("\nRunning test transactions...")
    deposit_result = deposit("12345", 100.00)
    print(f"Deposit Result: {deposit_result}")

    withdraw_result = withdraw("12345", 50.00)
    print(f"Withdraw Result: {withdraw_result}")

    transfer_result = transfer("12345", "67890", 25.00)
    print(f"Transfer Result: {transfer_result}")

    paybill_result = pay_bill("12345", 10.00)
    print(f"Pay Bill Result: {paybill_result}")

    change_result = change_plan("12345", "premium")
    print(f"Change Plan Result: {change_result}")
