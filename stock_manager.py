# functioality for managing adding/removing stocks
import yfinance as yf
import streamlit as st
from portfolio import save_portfolio

def remove_stock():
    """Handles removing stocks from the portfolio."""
    st.subheader("Remove Stock from Portfolio")

    if st.session_state["portfolio"]:
        stock_to_remove = st.selectbox("Select stock to remove", list(st.session_state["portfolio"].keys()))
        if st.button("❌ Remove Stock"):
            del st.session_state["portfolio"][stock_to_remove]
            save_portfolio(st.session_state["portfolio"])
            st.success(f"{stock_to_remove} removed from portfolio!")
            st.rerun()
    else:
        st.warning("No stocks to remove.")

def get_stock_ticker(company_name):
    try:
        stock = yf.Ticker(company_name)
        return stock.ticker
    except:
        return None

def add_stock2():
    """Handles adding stocks to the portfolio with ticker lookup and weighted average price calculation."""
    st.subheader("Add Stock to Portfolio")
    col1, col2, col3 = st.columns(3)
    with col1:
        company_name = st.text_input("Company Name / Stock Ticker", placeholder="Apple or AAPL").upper()
    with col2:
        new_quantity = st.number_input("Quantity", min_value=0.0001, step=0.0001, format="%.4f")  # ✅ Allow fractional shares
    with col3:
        new_buy_price = st.number_input("Buy Price per Share", min_value=0.01, step=0.01, format="%.2f")  # ✅ Allow cents

    if st.button("➕ Add Stock"):
        if company_name:
            stock_ticker = get_stock_ticker(company_name)  # Convert company name to ticker
            if not stock_ticker:
                st.error(f"❌ Could not find a stock ticker for '{company_name}'. Try again.")
                return
            # ✅ Handle multiple purchases of the same stock
            if stock_ticker in st.session_state["portfolio"]:
                existing = st.session_state["portfolio"][stock_ticker]
                # Calculate weighted average price
                total_shares = existing["quantity"] + new_quantity
                weighted_buy_price = ((existing["quantity"] * existing["buy_price"]) + 
                                      (new_quantity * new_buy_price)) / total_shares
                # Update the existing stock entry
                st.session_state["portfolio"][stock_ticker] = {
                    "quantity": round(total_shares, 4),  # ✅ Round to 4 decimal places
                    "buy_price": round(weighted_buy_price, 2),  # ✅ Round to 2 decimal places
                }
            else:
                # Add a new entry
                st.session_state["portfolio"][stock_ticker] = {
                    "quantity": round(new_quantity, 4),  # ✅ Store fractional shares
                    "buy_price": round(new_buy_price, 2),
                }

            # Save changes and refresh
            save_portfolio(st.session_state["portfolio"])
            st.success(f"{stock_ticker} updated in portfolio! ({total_shares} shares at ${round(weighted_buy_price, 2)})")
            st.rerun()

def add_stock():
    """Handles adding stocks to the portfolio with ticker lookup and weighted average price calculation."""
    st.subheader("Add Stock to Portfolio")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        company_name = st.text_input("Company Name / Stock Ticker", placeholder="Apple or AAPL").upper()
    with col2:
        new_quantity = st.number_input("Quantity", min_value=0.0001, step=0.0001, format="%.4f")  # ✅ Allow fractional shares
    with col3:
        new_buy_price = st.number_input("Buy Price per Share", min_value=0.01, step=0.01, format="%.2f")  # ✅ Allow cents

    if st.button("➕ Add Stock"):
        if company_name:
            stock_ticker = get_stock_ticker(company_name)  # Convert company name to ticker
            if not stock_ticker:
                st.error(f"❌ Could not find a stock ticker for '{company_name}'. Try again.")
                return
            
            # ✅ Ensure total_shares is always defined
            total_shares = new_quantity
            weighted_buy_price = new_buy_price

            # ✅ Handle multiple purchases of the same stock
            if stock_ticker in st.session_state["portfolio"]:
                existing = st.session_state["portfolio"][stock_ticker]
                
                # Calculate weighted average price
                total_shares = existing["quantity"] + new_quantity
                weighted_buy_price = ((existing["quantity"] * existing["buy_price"]) + 
                                      (new_quantity * new_buy_price)) / total_shares

            # ✅ Update or create stock entry
            st.session_state["portfolio"][stock_ticker] = {
                "quantity": round(total_shares, 4),  # ✅ Store fractional shares
                "buy_price": round(weighted_buy_price, 2),
            }

            # Save changes and refresh
            save_portfolio(st.session_state["portfolio"])
            st.success(f"{stock_ticker} updated in portfolio! ({total_shares} shares at ${round(weighted_buy_price, 2)})")
            st.rerun()
