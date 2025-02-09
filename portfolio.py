# Handles portfolio logic (load, save, modify)

import json
import os

PORTFOLIO_FILE = "portfolio.json"

def load_portfolio():
    """Load portfolio from JSON file."""
    if os.path.exists(PORTFOLIO_FILE):
        try:
            with open(PORTFOLIO_FILE, "r") as file:
                data = json.load(file)
                if isinstance(data, dict):
                    return data
        except (json.JSONDecodeError, ValueError):
            print("Warning: portfolio.json is empty or corrupted. Resetting...")
    return {}

def save_portfolio(portfolio):
    """Save portfolio to JSON file."""
    with open(PORTFOLIO_FILE, "w") as file:
        json.dump(portfolio, file, indent=4)

