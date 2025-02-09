# Utility functions (profit calculations, etc.)
#
def calculate_portfolio(portfolio, stock_prices):
    """Calculate portfolio statistics including profit/loss."""
    portfolio_data = []
    for stock, details in portfolio.items():
        quantity = details["quantity"]
        buy_price = details["buy_price"]
        current_price = stock_prices.get(stock, 0)
        total_cost = quantity * buy_price
        print(f"quantity is {quantity}")
        print(f"current price is {current_price}")
        current_value = quantity * current_price
        profit_loss = current_value - total_cost
        percent_change = ((current_value - total_cost) / total_cost) * 100 if total_cost > 0 else 0

        portfolio_data.append({
            "Stock": stock,
            "Quantity": quantity,
            "Buy Price": buy_price,
            "Current Price": round(current_price, 2) if current_price else "N/A",
            "Total Cost ($)": round(total_cost, 2),
            "Current Value ($)": round(current_value, 2),
            "Profit/Loss ($)": round(profit_loss, 2),
            "Change (%)": round(percent_change, 2),
        })

    return portfolio_data

