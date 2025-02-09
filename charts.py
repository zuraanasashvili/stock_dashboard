import streamlit as st
import plotly.express as px
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

def show_portfolio_pie_chart(portfolio_data):
    """Displays a pie chart of portfolio allocation based on stock value."""
    if not portfolio_data:
        st.warning("No data available for the pie chart.")
        return
    df = pd.DataFrame(portfolio_data)
    # Ensure we have the necessary column
    if "Current Value ($)" in df.columns:
        fig = px.pie(df, values="Current Value ($)", names="Stock", title="📊 Portfolio Allocation")
        st.plotly_chart(fig)
    else:
        st.warning("Portfolio data missing required fields for visualization.")


def show_stock_price_history(selected_stock, time_period):
    """Displays a time-series chart for a selected stock's price history based on user-selected period."""
    if not selected_stock:
        return

    st.subheader(f"📈 {selected_stock} Price History ({time_period})")

    # Fetch historical stock data based on selected period
    stock_data = yf.Ticker(selected_stock).history(period=time_period)

    if stock_data.empty:
        st.warning(f"No historical data found for {selected_stock}.")
        return

    # Create a time-series line chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data["Close"], mode="lines", name="Closing Price"))
    fig.update_layout(title=f"{selected_stock} Stock Price History ({time_period})", xaxis_title="Date", yaxis_title="Price")

    st.plotly_chart(fig)

def show_portfolio_performance(portfolio, time_period):
    """Displays a time-series chart showing the total portfolio value over time."""
    if not portfolio:
        st.warning("No stocks in portfolio.")
        return

    st.subheader(f"📈 Portfolio Performance Over Time ({time_period})")

    interval = "1d"  
    if time_period == "15m":
        interval = "1m"
    elif time_period in ["5d", "1mo"]:
        interval = "1h"

    portfolio_data = {}
    for stock, details in portfolio.items():
        stock_data = yf.Ticker(stock).history(period=time_period, interval=interval)
        if not stock_data.empty:
            stock_data["Value"] = stock_data["Close"] * details["quantity"]
            portfolio_data[stock] = stock_data["Value"]

    if not portfolio_data:
        st.warning("No historical data available for the portfolio.")
        return

    portfolio_df = pd.DataFrame(portfolio_data)
    portfolio_df["Total Portfolio Value"] = portfolio_df.sum(axis=1)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=portfolio_df.index, y=portfolio_df["Total Portfolio Value"], mode="lines", name="Portfolio Value"))
    fig.update_layout(title=f"📊 Portfolio Performance ({time_period})", xaxis_title="Date", yaxis_title="Total Value ($)")

    st.plotly_chart(fig)

def show_profit_loss_chart(portfolio_df):
    """Displays a bar chart showing Profit/Loss for each stock."""
    fig = px.bar(
        portfolio_df[:-1],  # Exclude TOTAL row
        x="Stock",
        y="Profit/Loss ($)",
        color="Profit/Loss ($)",
        title="📊 Profit/Loss Per Stock",
    )
    st.plotly_chart(fig)


def show_portfolio_vs_sp500(portfolio, time_period):
    """Displays a chart comparing portfolio performance against the S&P 500 (SPY ETF)."""
    if not portfolio:
        st.warning("No stocks in portfolio.")
        return

    st.subheader(f"📊 Portfolio vs. S&P 500 ({time_period})")

    interval = "1d"  
    if time_period == "15m":
        interval = "1m"
    elif time_period in ["5d", "1mo"]:
        interval = "1h"

    # Fetch S&P 500 (SPY ETF) data
    spy_data = yf.Ticker("SPY").history(period=time_period, interval=interval)
    if spy_data.empty:
        st.warning("Could not fetch S&P 500 data.")
        return

    # Fetch portfolio stock data
    portfolio_data = {}
    for stock, details in portfolio.items():
        stock_data = yf.Ticker(stock).history(period=time_period, interval=interval)
        if not stock_data.empty:
            stock_data["Value"] = stock_data["Close"] * details["quantity"]
            portfolio_data[stock] = stock_data["Value"]

    if not portfolio_data:
        st.warning("No historical data available for the portfolio.")
        return

    # Create a DataFrame for portfolio performance
    portfolio_df = pd.DataFrame(portfolio_data)
    portfolio_df["Total Portfolio Value"] = portfolio_df.sum(axis=1)

    # Normalize to start at 100 for comparison
    portfolio_df["Portfolio Performance"] = (portfolio_df["Total Portfolio Value"] / portfolio_df["Total Portfolio Value"].iloc[0]) * 100
    spy_data["S&P 500 Performance"] = (spy_data["Close"] / spy_data["Close"].iloc[0]) * 100

    # Create a comparison chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=portfolio_df.index, y=portfolio_df["Portfolio Performance"], mode="lines", name="Portfolio"))
    fig.add_trace(go.Scatter(x=spy_data.index, y=spy_data["S&P 500 Performance"], mode="lines", name="S&P 500 (SPY)", line=dict(dash="dot")))

    fig.update_layout(title=f"📊 Portfolio vs. S&P 500 ({time_period})", xaxis_title="Date", yaxis_title="Performance (Normalized)")

    st.plotly_chart(fig)
