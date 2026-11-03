import csv
import importlib
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CONSTITUENTS_FILE = BASE_DIR / "constituents.csv"
OUTPUT_FILE = BASE_DIR / "portfolio_summary.csv"


def load_companies():
    companies = {}
    try:
        with CONSTITUENTS_FILE.open("r", newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            if not reader.fieldnames or "Symbol" not in reader.fieldnames:
                raise ValueError("The CSV must contain a 'Symbol' column.")

            for row in reader:
                symbol = (row.get("Symbol") or "").strip().upper()
                name = (row.get("Security") or "").strip()
                if symbol:
                    companies[symbol] = name or symbol
    except FileNotFoundError:
        print(f"Error: Could not find {CONSTITUENTS_FILE.name}.")
        print("Keep constituents.csv in the same folder as portfolio.py.")
        raise SystemExit(1)
    except (OSError, csv.Error, ValueError) as error:
        print(f"Could not read the company list: {error}")
        raise SystemExit(1)

    return companies


def get_current_price(ticker):
    try:
        yf = importlib.import_module("yfinance")

        stock = yf.Ticker(ticker)
        price = stock.fast_info.get("lastPrice")
        if price is None:
            history = stock.history(period="1d")
            if not history.empty:
                price = history["Close"].dropna().iloc[-1]

        if price is not None and float(price) > 0:
            return float(price)
    except Exception:
        # Network, package, or data-provider errors are handled by manual input.
        pass

    return None


def ask_positive_number(prompt):
    while True:
        try:
            value = float(input(prompt).strip())
            if value > 0:
                return value
            print("Please enter a number greater than zero.")
        except ValueError:
            print("Please enter a valid number.")


def collect_positions(companies):
    positions = {}
    print("\nEnter your stock holdings.")
    print("Type DONE when you have finished adding stocks.\n")

    while True:
        ticker = input("Stock ticker: ").strip().upper()
        if ticker == "DONE":
            break
        if not ticker:
            print("Ticker cannot be empty.")
            continue
        if ticker not in companies:
            print("Ticker not found in constituents.csv. Please use a listed ticker.")