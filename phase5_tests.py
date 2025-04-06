import unittest
from unittest.mock import patch, mock_open
from io import StringIO
from accountmanagement import AccountManager
from print_error import log_constraint_error
from read import read_old_bank_accounts
from write import write_new_current_accounts
from authsystem import login, is_admin
from transactionsystem import TransactionSystem

def build_account_line(account_number, name, status, balance, txns="00000"):
    # Expected format:
    # - Account number: 5 chars (left-aligned)
    # - Space: 1 char
    # - Name: 20 chars (left-aligned)
    # - Space: 1 char
    # - Status: 1 char
    # - Space: 1 char
    # - Balance: 10 chars (left-aligned)
    # - Space: 1 char
    # - Transactions: 5 chars (left-aligned)
    # Total (excluding newline): 5+1+20+1+1+1+10+1+5 = 45
    return f"{account_number:<5} {name:<20} {status} {balance:<10} {txns}\n"

class TestPrintError(unittest.TestCase):
    def test_log_constraint_error(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            log_constraint_error("Withdraw", "Insufficient funds")
            self.assertIn("ERROR: Insufficient funds: Withdraw", fake_out.getvalue())

class TestRead(unittest.TestCase):
    def test_invalid_length(self):
        data = "short line\n"
        with patch("builtins.open", mock_open(read_data=data)):
            with patch("sys.stdout", new=StringIO()) as fake_out:
                read_old_bank_accounts("fake.txt")
                self.assertIn("Invalid length", fake_out.getvalue())

    def test_invalid_status(self):
        # Build a line with an invalid status ("Z")
        data = build_account_line("12345", "John Doe", "Z", "000000.00")
        assert len(data.strip('\n')) == 45, f"Line length wrong: {len(data.strip())}"
        with patch("builtins.open", mock_open(read_data=data)):
            with patch("sys.stdout", new=StringIO()) as fake_out:
                read_old_bank_accounts("fake.txt")
                self.assertIn("Invalid status", fake_out.getvalue())

    def test_invalid_balance_format(self):
        # Build a line with an invalid balance format ("0000x.00")
        data = build_account_line("12345", "John Doe", "A", "0000x.00")
        assert len(data.strip('\n')) == 45, f"Line length wrong: {len(data.strip())}"
        with patch("builtins.open", mock_open(read_data=data)):
            with patch("sys.stdout", new=StringIO()) as fake_out:
                read_old_bank_accounts("fake.txt")
                self.assertIn("Invalid balance format", fake_out.getvalue())

    def test_negative_balance(self):
        # Build a line with a negative balance ("-0100.00")
        data = build_account_line("12345", "John Doe", "A", "-0100.00")
        assert len(data.strip('\n')) == 45, f"Line length wrong: {len(data.strip())}"
        with patch("builtins.open", mock_open(read_data=data)):
            with patch("sys.stdout", new=StringIO()) as fake_out:
                read_old_bank_accounts("fake.txt")
                self.assertIn("Negative balance", fake_out.getvalue())

class TestWrite(unittest.TestCase):
    def test_invalid_account_number(self):
        accounts = [{'account_number': 'abcde', 'name': 'User', 'status': 'A',
                     'balance': 100.0, 'total_transactions': 0}]
        with self.assertRaises(ValueError):
            write_new_current_accounts(accounts, "file.txt")

    def test_name_too_long(self):
        accounts = [{'account_number': '12345', 'name': 'A'*25, 'status': 'A',
                     'balance': 100.0, 'total_transactions': 0}]
        with self.assertRaises(ValueError):
            write_new_current_accounts(accounts, "file.txt")

    def test_invalid_status(self):
        accounts = [{'account_number': '12345', 'name': 'User', 'status': 'Z',
                     'balance': 100.0, 'total_transactions': 0}]
        with self.assertRaises(ValueError):
            write_new_current_accounts(accounts, "file.txt")

    def test_invalid_balance_type(self):
        accounts = [{'account_number': '12345', 'name': 'User', 'status': 'A',
                     'balance': 'invalid', 'total_transactions': 0}]
        with self.assertRaises(ValueError):
            write_new_current_accounts(accounts, "file.txt")

    def test_balance_out_of_range(self):
        accounts = [{'account_number': '12345', 'name': 'User', 'status': 'A',
                     'balance': 100000.0, 'total_transactions': 0}]
        with self.assertRaises(ValueError):
            write_new_current_accounts(accounts, "file.txt")

class TestAuthSystem(unittest.TestCase):
    @patch('read.read_old_bank_accounts')
    def test_login_success(self, mock_read):
        mock_read.return_value = [{'account_number': '1', 'name': 'Admin', 'status': 'A'}]
        self.assertIsNotNone(login('00001', 'Admin'))

    @patch('read.read_old_bank_accounts')
    def test_login_fail_name(self, mock_read):
        mock_read.return_value = [{'account_number': '1', 'name': 'Admin', 'status': 'A'}]
        self.assertIsNone(login('00001', 'WrongName'))

    @patch('read.read_old_bank_accounts')
    def test_login_inactive(self, mock_read):
        mock_read.return_value = [{'account_number': '1', 'name': 'Admin', 'status': 'D'}]
        self.assertIsNone(login('00001', 'Admin'))

    @patch('read.read_old_bank_accounts')
    def test_is_admin_true(self, mock_read):
        mock_read.return_value = [{'account_number': '1', 'name': 'Admin'}]
        self.assertTrue(is_admin('00001'))

    @patch('read.read_old_bank_accounts')
    def test_is_admin_false(self, mock_read):
        mock_read.return_value = [{'account_number': '2', 'name': 'User'}]
        self.assertFalse(is_admin('00002'))

class TestTransactionSystem(unittest.TestCase):
    @patch("transactionsystem.input")
    @patch("transactionsystem.login")
    @patch("transactionsystem.read_old_bank_accounts")
    @patch("transactionsystem.write_new_current_accounts")
    def test_interactive_withdraw_success(self, mock_write, mock_read, mock_login, mock_input):
        ts = TransactionSystem()
        ts.session_withdraw_total = 0
        mock_input.side_effect = ['n', 'User', '12345', '100']
        mock_login.return_value = {
            'account_number': '12345', 'name': 'User', 'status': 'A',
            'balance': 200, 'account_type': 'basic'
        }
        mock_read.return_value = [{'account_number': '12345', 'balance': 200}]

        result = ts.interactive_withdraw()
        print("READ MOCK RETURN VALUE:", mock_read.return_value)
        self.assertTrue(result)
        mock_read.assert_called_once()
        mock_write.assert_called_once()
        written_accounts = mock_write.call_args[0][0]
        self.assertEqual(written_accounts[0]['balance'], 100.0)

    @patch("transactionsystem.input")
    @patch("transactionsystem.login")
    def test_interactive_transfer_success(self, mock_login, mock_input):
        ts = TransactionSystem()
        mock_input.side_effect = ['n', 'User', '12345', '67890', '50']
        mock_login.return_value = {
            'account_number': '12345', 'name': 'User', 'status': 'A',
            'balance': 200, 'account_type': 'basic'
        }
        with patch("transactionsystem.read_old_bank_accounts", return_value=[
            {'account_number': '12345', 'balance': 200},
            {'account_number': '67890', 'balance': 100}
        ]):
            with patch("transactionsystem.write_new_current_accounts"):
                self.assertTrue(ts.interactive_transfer())

    @patch("transactionsystem.input")
    @patch("transactionsystem.login")
    def test_interactive_pay_bill_success(self, mock_login, mock_input):
        ts = TransactionSystem()
        mock_input.side_effect = ['n', 'User', '12345', 'Fast Internet, Inc. (FI)', '100']
        mock_login.return_value = {
            'account_number': '12345', 'name': 'User', 'status': 'A',
            'balance': 200, 'account_type': 'basic'
        }
        with patch("transactionsystem.read_old_bank_accounts", return_value=[{'account_number': '12345', 'balance': 200}]):
            with patch("transactionsystem.write_new_current_accounts"):
                self.assertTrue(ts.interactive_pay_bill())

    @patch("transactionsystem.input")
    @patch("transactionsystem.login")
    def test_interactive_change_plan_success(self, mock_login, mock_input):
        ts = TransactionSystem()
        mock_input.side_effect = ['y', 'User', '12345']
        mock_login.return_value = {
            'account_number': '12345', 'name': 'User', 'status': 'A',
            'account_type': 'SP'
        }
        with patch("transactionsystem.read_old_bank_accounts", return_value=[{'account_number': '12345', 'account_type': 'SP'}]):
            with patch("transactionsystem.write_new_current_accounts"):
                self.assertTrue(ts.interactive_change_plan())

    @patch("transactionsystem.input")
    @patch("transactionsystem.login")
    def test_interactive_deposit_success(self, mock_login, mock_input):
        ts = TransactionSystem()
        mock_input.side_effect = ['n', 'User', '12345', '50']
        mock_login.return_value = {'account_number': '12345', 'name': 'User', 'status': 'A'}
        self.assertTrue(ts.interactive_deposit())
        
class TestTransactionSystemEdgeCases(unittest.TestCase):
    @patch("transactionsystem.input")
    @patch("transactionsystem.login")
    def test_withdraw_exceeds_session_limit(self, mock_login, mock_input):
        ts = TransactionSystem()
        ts.session_withdraw_total = 450
        mock_input.side_effect = ['n', 'User', '12345', '100']
        mock_login.return_value = {
            'account_number': '12345', 'name': 'User', 'status': 'A',
            'balance': 1000, 'account_type': 'basic'
        }
        with patch("transactionsystem.read_old_bank_accounts", return_value=[{'account_number': '12345', 'balance': 1000}]):
            with patch("transactionsystem.write_new_current_accounts"):
                result = ts.interactive_withdraw()
                self.assertFalse(result)

    @patch("transactionsystem.input")
    @patch("transactionsystem.login")
    def test_transfer_invalid_destination(self, mock_login, mock_input):
        ts = TransactionSystem()
        mock_input.side_effect = ['n', 'User', '12345', '99999', '50']
        mock_login.return_value = {
            'account_number': '12345', 'name': 'User', 'status': 'A',
            'balance': 500, 'account_type': 'basic'
        }
        with patch("transactionsystem.read_old_bank_accounts", return_value=[{'account_number': '12345', 'balance': 500}]):
            with patch("transactionsystem.write_new_current_accounts"):
                result = ts.interactive_transfer()
                self.assertFalse(result)

    @patch("transactionsystem.input")
    @patch("transactionsystem.login")
    def test_change_plan_not_student(self, mock_login, mock_input):
        ts = TransactionSystem()
        mock_input.side_effect = ['y', 'User', '12345']
        mock_login.return_value = {
            'account_number': '12345', 'name': 'User', 'status': 'A',
            'account_type': 'NP'
        }
        with patch("transactionsystem.read_old_bank_accounts", return_value=[{'account_number': '12345', 'account_type': 'NP'}]):
            with patch("transactionsystem.write_new_current_accounts"):
                result = ts.interactive_change_plan()
                self.assertFalse(result)

class TestAccountManagement(unittest.TestCase):
    @patch("accountmanagement.input")
    @patch("accountmanagement.login")
    @patch("accountmanagement.is_admin", return_value=True)
    @patch("accountmanagement.read_old_bank_accounts")
    @patch("accountmanagement.write_new_current_accounts")
    def test_create_account_duplicate_number(self, mock_write, mock_read, mock_is_admin, mock_login, mock_input):
        am = AccountManager()
        mock_input.side_effect = ['y', '00001', 'Admin', 'Test User', '12345', 'basic', '1000.00']
        mock_read.return_value = [{'account_number': '12345'}]
        mock_login.return_value = {'account_number': '00001', 'name': 'Admin', 'status': 'A', 'account_type': 'admin'}
        result = am.create_account()
        self.assertFalse(result)

    @patch("accountmanagement.input")
    @patch("accountmanagement.login")
    @patch("accountmanagement.is_admin", return_value=True)
    @patch("accountmanagement.read_old_bank_accounts")
    @patch("accountmanagement.write_new_current_accounts")
    def test_disable_account_success(self, mock_write, mock_read, mock_is_admin, mock_login, mock_input):
        am = AccountManager()
        mock_input.side_effect = ['y', '00001', 'Admin', 'TargetUser', '12345']
        mock_read.return_value = [{'account_number': '12345', 'name': 'TargetUser', 'status': 'A', 'total_transactions': 0}]
        mock_login.return_value = {'account_number': '00001', 'name': 'Admin', 'status': 'A', 'account_type': 'admin'}
        result = am.disable_account()
        self.assertTrue(result)

    @patch("accountmanagement.input")
    @patch("accountmanagement.login")
    @patch("accountmanagement.is_admin", return_value=True)
    @patch("accountmanagement.read_old_bank_accounts")
    @patch("accountmanagement.write_new_current_accounts")
    def test_delete_account_name_mismatch(self, mock_write, mock_read, mock_is_admin, mock_login, mock_input):
        am = AccountManager()
        mock_input.side_effect = ['y', '00001', 'Admin', 'WrongName', '12345']
        mock_read.return_value = [{'account_number': '12345', 'name': 'CorrectName', 'status': 'A', 'total_transactions': 0}]
        mock_login.return_value = {'account_number': '00001', 'name': 'Admin', 'status': 'A', 'account_type': 'admin'}
        result = am.delete_account()
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()
