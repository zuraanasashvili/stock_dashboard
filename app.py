import streamlit as st
import pandas as pd
from portfolio import load_portfolio
from data_fetch import get_stock_prices
from functions import calculate_portfolio
from stock_manager import add_stock, remove_stock  # ✅ Import new functions
from charts import show_portfolio_pie_chart, show_stock_price_history, show_portfolio_performance, show_profit_loss_chart, show_portfolio_vs_sp500

# --- INITIALIZE PORTFOLIO ---
if "portfolio" not in st.session_state:
    st.session_state["portfolio"] = load_portfolio()

st.title("📈 Stock Portfolio Tracker")

# --- DISPLAY PORTFOLIO ---
st.subheader("Current Portfolio")

if not st.session_state["portfolio"]:
    st.warning("No stocks in portfolio.")
else:
    stock_prices = get_stock_prices(st.session_state["portfolio"].keys())
    portfolio_data = calculate_portfolio(st.session_state["portfolio"], stock_prices)
    portfolio_df = pd.DataFrame(portfolio_data)
    # ✅ Calculate total portfolio cost and value
    total_cost = portfolio_df["Total Cost ($)"].sum()
    total_value = portfolio_df["Current Value ($)"].sum()

    # ✅ Calculate percentage change for the entire portfolio
    if total_cost > 0:
        total_change = ((total_value - total_cost) / total_cost) * 100
    else:
        total_change = 0  # Prevent division by zero

    # ✅ Add a Total Row
    total_row = pd.DataFrame({
        "Stock": ["TOTAL"],
        "Quantity": [portfolio_df["Quantity"].sum()],
        "Buy Price": ["-"],
        "Current Price": ["-"],
        "Total Cost ($)": [portfolio_df["Total Cost ($)"].sum()],
        "Current Value ($)": [portfolio_df["Current Value ($)"].sum()],
        "Profit/Loss ($)": [portfolio_df["Profit/Loss ($)"].sum()],
        "Change (%)": [round(total_change, 2)] # Avoid averaging percentage change
    })

    # Append the total row to the DataFrame
    portfolio_df = pd.concat([portfolio_df, total_row], ignore_index=True)
    st.dataframe(portfolio_df)

    # show_profit_loss_chart(portfolio_data)

    show_portfolio_pie_chart(portfolio_data)

    st.subheader("📊 Stock Price History")
    col1, col2 = st.columns(2)
    with col1:
        selected_stock = st.selectbox("Select Stock", list(st.session_state["portfolio"].keys()))

    with col2:
        time_period = st.selectbox("Select Time Period", ["15min", "5d", "1mo", "6mo", "1y", "5y"], index=3)

    show_stock_price_history(selected_stock, time_period)

    st.subheader("📊 Portfolio Performance")
    portfolio_time_period = st.selectbox("Select Portfolio Time Period", ["15m", "5d", "1mo", "6mo", "1y", "5y"], index=3)
    show_portfolio_performance(st.session_state["portfolio"], portfolio_time_period)

    # ✅ Show Portfolio vs. S&P 500 Chart
    st.subheader("📊 Portfolio vs. S&P 500")
    benchmark_time_period = st.selectbox("Select Benchmark Time Period", ["15m", "5d", "1mo", "6mo", "1y", "5y"], index=3)
    show_portfolio_vs_sp500(st.session_state["portfolio"], benchmark_time_period)

# --- ADD/REMOVE STOCK SECTION (Moved to stock_manager.py) ---
add_stock()
remove_stock()
