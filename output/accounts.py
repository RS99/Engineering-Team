# accounts.py

class Transaction:
    """
    A class to represent a transaction in the trading account.
    """

    def __init__(self, action: str, quantity: int, symbol: str, price: float):
        """
        Initializes a new transaction.

        :param action: The action taken ('buy' or 'sell').
        :param quantity: Number of shares involved in the transaction.
        :param symbol: The stock symbol for the transaction.
        :param price: Price per share at the time of transaction.
        """
        self.action = action
        self.quantity = quantity
        self.symbol = symbol
        self.price = price  # The execution price of the shares


class Account:
    """
    A class to represent a user's trading account.
    """

    def __init__(self, user_id: str):
        """
        Initializes a new trading account for a user.

        :param user_id: The unique identifier for the user.
        """
        self.user_id = user_id
        self.balance = 0.0
        self.initial_deposit = 0.0 # Track initial deposits to calculate profit/loss accurately
        self.holdings = {}  # Dictionary to hold stock symbols as keys and share quantity as values
        self.transactions = []  # List to keep track of transactions

    def deposit(self, amount: float) -> None:
        """
        Deposit funds into the user's account.

        :param amount: The amount of money to deposit.
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        # Only add to initial_deposit for the very first deposit or a specific "initial" one.
        # For a simple system, let's consider any deposit as increasing the "invested" amount for P/L calculation.
        # A more complex system might differentiate initial capital vs. subsequent top-ups.
        # For this design, let's make initial_deposit represent total cash invested by user.
        self.initial_deposit += amount 

    def withdraw(self, amount: float) -> None:
        """
        Withdraw funds from the user's account.

        :param amount: The amount of money to withdraw.
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if self.balance - amount < 0:
            raise ValueError("Insufficient funds for withdrawal.")
        self.balance -= amount
        # Also decrease initial_deposit if funds are withdrawn that originated from user's capital.
        # This simplifies the P/L calculation by keeping track of net cash invested.
        self.initial_deposit -= amount
        if self.initial_deposit < 0:
            self.initial_deposit = 0 # Cannot have negative initial deposit

    def buy_shares(self, symbol: str, quantity: int) -> None:
        """
        Buy shares of a specific stock.

        :param symbol: The stock symbol to buy.
        :param quantity: The number of shares to buy.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        
        price_per_share = get_share_price(symbol)
        if price_per_share == 0.0:
            raise ValueError(f"Could not get price for symbol: {symbol}")

        total_cost = price_per_share * quantity
        
        if total_cost > self.balance:
            raise ValueError("Insufficient funds to buy shares.")
        
        self.balance -= total_cost
        self.holdings[symbol] = self.holdings.get(symbol, 0) + quantity
        self.transactions.append(Transaction('buy', quantity, symbol, price_per_share))

    def sell_shares(self, symbol: str, quantity: int) -> None:
        """
        Sell shares of a specific stock.

        :param symbol: The stock symbol to sell.
        :param quantity: The number of shares to sell.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        
        if symbol not in self.holdings or self.holdings[symbol] < quantity:
            raise ValueError(f"Not enough shares of {symbol} to sell.")
        
        price_per_share = get_share_price(symbol)
        if price_per_share == 0.0:
            raise ValueError(f"Could not get price for symbol: {symbol}")

        total_revenue = price_per_share * quantity
        
        self.holdings[symbol] -= quantity
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]  # Remove the symbol if no shares are left
        self.balance += total_revenue
        self.transactions.append(Transaction('sell', quantity, symbol, price_per_share))

    def calculate_portfolio_value(self) -> float:
        """
        Calculate the total value of the user's portfolio.
        This includes cash balance and the current market value of holdings.

        :return: The total value of the portfolio.
        """
        value = self.balance
        for symbol, quantity in self.holdings.items():
            current_price = get_share_price(symbol)
            if current_price == 0.0:
                # If price cannot be fetched, we cannot value this holding.
                # For a simulation, we might want to log this or use the last known price.
                # For this simple implementation, we'll treat it as 0 for valuation.
                print(f"Warning: Could not get current price for {symbol}. Valuing as 0 for portfolio calculation.")
            value += current_price * quantity
        return value

    def calculate_profit_or_loss(self) -> float:
        """
        Calculate the profit or loss from the initial deposit.
        Profit/Loss = Current Portfolio Value - Net Cash Invested (initial_deposit)

        :return: The profit or loss as a float value.
        """
        return self.calculate_portfolio_value() - self.initial_deposit

    def report_holdings(self) -> dict:
        """
        Report the current holdings of the user.

        :return: A dictionary of the user's holdings (symbol: quantity).
        """
        return self.holdings.copy() # Return a copy to prevent external modification

    def report_profit_or_loss(self) -> float:
        """
        Report the current profit or loss of the user.

        :return: The profit or loss amount.
        """
        return self.calculate_profit_or_loss()

    def list_transactions(self) -> list:
        """
        List all transactions made by the user.

        :return: A list of Transaction objects.
        """
        return self.transactions.copy() # Return a copy to prevent external modification


def get_share_price(symbol: str) -> float:
    """
    Get the current price of a given stock symbol.
    This is a test implementation returning fixed prices.
    In a real system, this would fetch live data.

    :param symbol: The stock symbol.
    :return: The current price of the stock, or 0.0 if not found.
    """
    prices = {
        'AAPL': 150.0,  # Example fixed prices
        'TSLA': 700.0,
        'GOOGL': 2800.0,
        'MSFT': 250.0, # Adding another example for variety
    }
    return prices.get(symbol, 0.0)  # Return 0.0 if symbol is not found or not in our test data