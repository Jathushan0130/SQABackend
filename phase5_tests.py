import unittest
from unittest.mock import patch
from io import StringIO
from print_error import log_constraint_error
from transactionsystem import TransactionSystem

class TestPrintError(unittest.TestCase):
    def test_log_constraint_error_withdraw(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            log_constraint_error("Withdraw", "Insufficient funds")
            self.assertIn("ERROR: Insufficient funds: Withdraw", fake_out.getvalue())

    def test_log_constraint_error_auth(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            log_constraint_error("Authentication", "Account not found")
            self.assertIn("ERROR: Account not found: Authentication", fake_out.getvalue())

    def test_log_constraint_error_delete(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            log_constraint_error("Delete Account", "Target name mismatch")
            self.assertIn("ERROR: Target name mismatch: Delete Account", fake_out.getvalue())
class TestWithdrawDecisionLoopCoverage(unittest.TestCase):
    @patch('builtins.input')
    @patch('transactionsystem.login')
    @patch('transactionsystem.read_old_bank_accounts')
    @patch('transactionsystem.write_new_current_accounts')
    def test_successful_withdraw_basic_user(self, mock_write, mock_read, mock_login, mock_input):
        ts = TransactionSystem()
        ts.session_withdraw_total = 0

        mock_input.side_effect = ['n', 'ActiveUser', '10001', '100']
        mock_login.return_value = {
            'account_number': '10001',
            'name': 'ActiveUser',
            'status': 'A',
            'balance': 200,
            'account_type': 'basic'
        }
        mock_read.return_value = [{'account_number': '10001', 'balance': 200}]

        result = ts.interactive_withdraw()
        print("READ MOCK RETURN VALUE:", mock_read.return_value) # To check what is being read
        self.assertTrue(result)
        mock_read.assert_called_once()
        mock_write.assert_called_once()

        # Check if balance was updated to 100
        written_accounts = mock_write.call_args[0][0]
        self.assertEqual(written_accounts[0]['balance'], 100)

    @patch('builtins.input')
    @patch('transactionsystem.login', return_value=None)
    def test_login_failure(self, mock_login, mock_input):
        ts = TransactionSystem()
        mock_input.side_effect = ['n', 'FakeUser', '99999', '100']
        result = ts.interactive_withdraw()
        self.assertFalse(result)

    @patch('builtins.input')
    @patch('transactionsystem.login')
    def test_exceeds_session_limit(self, mock_login, mock_input):
        ts = TransactionSystem()
        ts.session_withdraw_total = 480
        mock_input.side_effect = ['n', 'ActiveUser', '10001', '50']
        mock_login.return_value = {
            'account_number': '10001',
            'name': 'ActiveUser',
            'status': 'A',
            'balance': 500,
            'account_type': 'basic'
        }
        result = ts.interactive_withdraw()
        self.assertFalse(result)

    @patch('builtins.input')
    @patch('transactionsystem.login')
    def test_insufficient_funds(self, mock_login, mock_input):
        ts = TransactionSystem()
        mock_input.side_effect = ['n', 'ActiveUser', '10001', '500']
        mock_login.return_value = {
            'account_number': '10001',
            'name': 'ActiveUser',
            'status': 'A',
            'balance': 300,
            'account_type': 'basic'
        }
        result = ts.interactive_withdraw()
        self.assertFalse(result)

    @patch('builtins.input')
    @patch('transactionsystem.login')
    @patch('transactionsystem.read_old_bank_accounts')
    @patch('transactionsystem.write_new_current_accounts')
    def test_admin_withdraw_success(self, mock_write, mock_read, mock_login, mock_input):
        ts = TransactionSystem()
        ts.session_withdraw_total = 0
        mock_input.side_effect = ['y', 'AdminUser', '00001', '100']
        mock_login.return_value = {
            'account_number': '00001',
            'name': 'AdminUser',
            'status': 'A',
            'balance': 1000,
            'account_type': 'admin'
        }
        mock_read.return_value = [{'account_number': '1', 'balance': 1000}]  # 00001 normalized to '1'

        result = ts.interactive_withdraw()
        self.assertTrue(result)
        mock_read.assert_called_once()
        mock_write.assert_called_once()

        # Confirm balance was updated
        written_accounts = mock_write.call_args[0][0]
        self.assertEqual(written_accounts[0]['balance'], 900)


if __name__ == '__main__':
    unittest.main()
