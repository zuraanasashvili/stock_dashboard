# Fetches stock prices using yfinance
import yfinance as yf

def get_stock_prices(tickers):
    """Fetch live stock prices from yfinance."""
    prices = {}
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            prices[ticker] = stock.history(period="1d")["Close"].iloc[-1]
        except:
            prices[ticker] = None  # Handle invalid stock symbols
    return prices
