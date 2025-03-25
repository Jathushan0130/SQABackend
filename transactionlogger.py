class TransactionLogger:
    def __init__(self, log_file: str = "transaction_log.txt"):
        self.log_file = log_file

    def log_transaction(self, transaction_code: str, account_holder: str, account_number: str, amount: float, misc: str) -> None:
        """
        Writes a transaction log line in the following fixed-width format:
        
        CC_AAAAAAAAAA_NNNNNN_PPPPPP_MM
        
        where:
          - CC is a 2-character transaction code (e.g. "01" for withdrawal)
          - AAAAAAAAAA is the account holder’s name (10 characters, left-justified)
          - NNNNNN is the bank account number (6 digits, zero-padded)
          - PPPPPP is the amount in cents (6 digits, zero-padded)
          - MM is miscellaneous info (2 characters)
        """
        # Format the account holder's name to 10 characters (left-justified)
        name_field = account_holder.ljust(10)[:10]
        # Convert the account number to an integer and format as a 6-digit zero-padded string.
        try:
            num = int(account_number)
        except ValueError:
            num = 0
        account_field = f"{num:06d}"
        # Convert the amount (in dollars) to cents and format as a 6-digit number.
        amount_cents = int(round(amount * 100))
        amount_field = f"{amount_cents:06d}"
        # Format miscellaneous field to 2 characters.
        misc_field = misc.ljust(2)[:2]

        line = f"{transaction_code}_{name_field}_{account_field}_{amount_field}_{misc_field}\n"
        with open(self.log_file, "a") as f:
            f.write(line)

    def end_session(self) -> None:
        """
        Writes an end-of-session record using transaction code "00" and prints a message.
        """
        # Here we use "END_OF_SE" for the account holder field (which will be truncated to 10 characters),
        # "000000" for the account number, 0.0 for the amount, and "ES" for miscellaneous.
        self.log_transaction("00", "END_OF_SE", "000000", 0.0, "ES")
        print(f"Session ended. Transaction log is available at: {self.log_file}")
