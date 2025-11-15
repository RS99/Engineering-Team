import gradio as gr
from accounts import Account, Transaction, get_share_price

# Initialize a single account for demonstration purposes
user_account = Account("demo_user")

def get_account_summary():
    """Returns a formatted string of the current account summary."""
    holdings_str = ", ".join([f"{symbol}: {qty}" for symbol, qty in user_account.report_holdings().items()]) if user_account.report_holdings() else "None"
    
    return (
        f"**User ID:** {user_account.user_id}\n"
        f"**Balance:** ${user_account.balance:.2f}\n"
        f"**Initial Investment (Net):** ${user_account.initial_deposit:.2f}\n"
        f"**Current Holdings:** {holdings_str}\n"
        f"**Portfolio Value:** ${user_account.calculate_portfolio_value():.2f}\n"
        f"**Profit/Loss:** ${user_account.calculate_profit_or_loss():.2f}"
    )

def deposit_funds(amount: float):
    """Handles depositing funds."""
    try:
        user_account.deposit(amount)
        return get_account_summary(), f"Successfully deposited ${amount:.2f}."
    except ValueError as e:
        return get_account_summary(), f"Error: {e}"

def withdraw_funds(amount: float):
    """Handles withdrawing funds."""
    try:
        user_account.withdraw(amount)
        return get_account_summary(), f"Successfully withdrew ${amount:.2f}."
    except ValueError as e:
        return get_account_summary(), f"Error: {e}"

def buy_shares(symbol: str, quantity: int):
    """Handles buying shares."""
    try:
        user_account.buy_shares(symbol.upper(), quantity)
        return get_account_summary(), f"Successfully bought {quantity} shares of {symbol.upper()}."
    except ValueError as e:
        return get_account_summary(), f"Error: {e}"

def sell_shares(symbol: str, quantity: int):
    """Handles selling shares."""
    try:
        user_account.sell_shares(symbol.upper(), quantity)
        return get_account_summary(), f"Successfully sold {quantity} shares of {symbol.upper()}."
    except ValueError as e:
        return get_account_summary(), f"Error: {e}"

def report_transactions():
    """Returns a formatted string of all transactions."""
    transactions = user_account.list_transactions()
    if not transactions:
        return "No transactions yet."
    
    report = []
    for i, t in enumerate(transactions):
        report.append(f"{i+1}. {t.action.capitalize()} {t.quantity} shares of {t.symbol} at ${t.price:.2f}/share.")
    return "\n".join(report)

def get_current_share_price(symbol: str):
    """Returns the current share price for a given symbol."""
    price = get_share_price(symbol.upper())
    if price == 0.0:
        return f"Could not find price for {symbol.upper()}."
    return f"Current price for {symbol.upper()}: ${price:.2f}"

with gr.Blocks() as demo:
    gr.Markdown("# Simple Trading Simulation Account")
    gr.Markdown("This demo provides a simple UI to interact with the `Account` backend.")

    with gr.Row():
        account_summary_output = gr.Markdown(get_account_summary(), label="Account Summary")
    
    message_output = gr.Textbox(label="Status Message", interactive=False)

    with gr.Tab("Funds Management"):
        gr.Markdown("## Deposit / Withdraw Funds")
        with gr.Row():
            deposit_amount = gr.Number(label="Deposit Amount", value=1000.0)
            deposit_btn = gr.Button("Deposit Funds")
            
        with gr.Row():
            withdraw_amount = gr.Number(label="Withdraw Amount", value=100.0)
            withdraw_btn = gr.Button("Withdraw Funds")

    with gr.Tab("Trade Shares"):
        gr.Markdown("## Buy / Sell Shares")
        with gr.Row():
            symbol_input_buy = gr.Textbox(label="Stock Symbol (e.g., AAPL)", value="AAPL")
            quantity_input_buy = gr.Number(label="Quantity to Buy", value=1)
            buy_btn = gr.Button("Buy Shares")
        
        with gr.Row():
            symbol_input_sell = gr.Textbox(label="Stock Symbol (e.g., AAPL)", value="AAPL")
            quantity_input_sell = gr.Number(label="Quantity to Sell", value=1)
            sell_btn = gr.Button("Sell Shares")

        with gr.Row():
            price_symbol_input = gr.Textbox(label="Check Price for Symbol", value="AAPL")
            get_price_btn = gr.Button("Get Current Price")
            current_price_output = gr.Textbox(label="Current Share Price", interactive=False)

    with gr.Tab("Reports"):
        gr.Markdown("## Account Reports")
        with gr.Row():
            transactions_btn = gr.Button("List All Transactions")
            
        transactions_output = gr.Textbox(label="Transaction History", interactive=False, lines=10)

    # Wire up interactions
    deposit_btn.click(
        deposit_funds, 
        inputs=[deposit_amount], 
        outputs=[account_summary_output, message_output]
    )
    withdraw_btn.click(
        withdraw_funds, 
        inputs=[withdraw_amount], 
        outputs=[account_summary_output, message_output]
    )
    buy_btn.click(
        buy_shares, 
        inputs=[symbol_input_buy, quantity_input_buy], 
        outputs=[account_summary_output, message_output]
    )
    sell_btn.click(
        sell_shares, 
        inputs=[symbol_input_sell, quantity_input_sell], 
        outputs=[account_summary_output, message_output]
    )
    transactions_btn.click(
        report_transactions, 
        outputs=[transactions_output]
    )
    get_price_btn.click(
        get_current_share_price,
        inputs=[price_symbol_input],
        outputs=[current_price_output]
    )

demo.launch()