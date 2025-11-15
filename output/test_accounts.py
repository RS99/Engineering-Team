import unittest
from accounts import Account, Transaction, get_share_price

class TestAccount(unittest.TestCase):
    def setUp(self):
        self.account = Account("user123")

    def test_initial_balance(self):
        self.assertEqual(self.account.balance, 0.0)

    def test_deposit(self):
        self.account.deposit(1000)
        self.assertEqual(self.account.balance, 1000.0)
        self.assertEqual(self.account.initial_deposit, 1000.0)

    def test_negative_deposit(self):
        with self.assertRaises(ValueError):
            self.account.deposit(-500)

    def test_withdraw(self):
        self.account.deposit(1000)
        self.account.withdraw(500)
        self.assertEqual(self.account.balance, 500.0)
        self.assertEqual(self.account.initial_deposit, 500.0)

    def test_withdraw_exceed_balance(self):
        self.account.deposit(500)
        with self.assertRaises(ValueError):
            self.account.withdraw(1000)

    def test_buy_shares(self):
        self.account.deposit(1000)
        self.account.buy_shares("AAPL", 3)
        self.assertEqual(self.account.holdings["AAPL"], 3)
        self.assertEqual(self.account.balance, 150.0)
        self.assertEqual(len(self.account.transactions), 1)
        self.assertEqual(self.account.transactions[0].action, "buy")

    def test_buy_shares_insufficient_funds(self):
        with self.assertRaises(ValueError):
            self.account.buy_shares("AAPL", 3)

    def test_sell_shares(self):
        self.account.deposit(1000)
        self.account.buy_shares("AAPL", 3)
        self.account.sell_shares("AAPL", 1)
        self.assertEqual(self.account.holdings["AAPL"], 2)
        self.assertEqual(len(self.account.transactions), 2)
        self.assertEqual(self.account.transactions[1].action, "sell")

    def test_sell_shares_not_enough(self):
        self.account.deposit(1000)
        self.account.buy_shares("AAPL", 3)
        with self.assertRaises(ValueError):
            self.account.sell_shares("AAPL", 4)

    def test_calculate_portfolio_value(self):
        self.account.deposit(1000)
        self.account.buy_shares("AAPL", 3)
        value = self.account.calculate_portfolio_value()
        self.assertEqual(value, 150.0 + 1000.0)

    def test_report_holdings(self):
        self.account.deposit(1000)
        self.account.buy_shares("AAPL", 3)
        holdings = self.account.report_holdings()
        self.assertEqual(holdings["AAPL"], 3)

    def test_report_profit_or_loss(self):
        self.account.deposit(1000)
        self.account.buy_shares("AAPL", 3)
        profit_loss = self.account.report_profit_or_loss()
        self.assertEqual(profit_loss, (150.0 + 1000.0) - 1000.0)

    def test_list_transactions(self):
        self.account.deposit(1000)
        self.account.buy_shares("AAPL", 3)
        transactions = self.account.list_transactions()
        self.assertEqual(len(transactions), 1)

if __name__ == "__main__":
    unittest.main()