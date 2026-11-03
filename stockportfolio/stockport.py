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
            continue
        if ticker in positions:
            print("That ticker is already in your portfolio.")
            continue

        shares = ask_positive_number("Number of shares: ")
        buy_price = ask_positive_number("Purchase price per share ($): ")

        current_price = get_current_price(ticker)
        if current_price is None:
            print(f"Could not retrieve a live price for {ticker}.")
            current_price = ask_positive_number(
                "Enter the current price per share ($): "
            )
            price_source = "Manual"
        else:
            print(f"Latest available price for {ticker}: ${current_price:,.2f}")
            price_source = "yfinance"

        positions[ticker] = {
            "company": companies[ticker],
            "shares": shares,
            "buy_price": buy_price,
            "current_price": current_price,
            "price_source": price_source,
        }
        print(f"Added {ticker}.\n")

    return positions


def calculate_summary(positions):
    rows = []
    total_invested = 0.0
    total_market_value = 0.0

    for ticker, holding in positions.items():
        invested = holding["shares"] * holding["buy_price"]
        market_value = holding["shares"] * holding["current_price"]
        gain_loss = market_value - invested
        gain_loss_percent = (gain_loss / invested) * 100 if invested else 0.0

        total_invested += invested
        total_market_value += market_value

        rows.append({
            "ticker": ticker,
            "company": holding["company"],
            "shares": holding["shares"],
            "buy_price": holding["buy_price"],
            "current_price": holding["current_price"],
            "invested": invested,
            "market_value": market_value,
            "gain_loss": gain_loss,
            "gain_loss_percent": gain_loss_percent,
            "price_source": holding["price_source"],
        })

    total_gain_loss = total_market_value - total_invested
    total_gain_loss_percent = (
        total_gain_loss / total_invested * 100 if total_invested else 0.0
    )

    totals = {
        "invested": total_invested,
        "market_value": total_market_value,
        "gain_loss": total_gain_loss,
        "gain_loss_percent": total_gain_loss_percent,
    }
    return rows, totals


def display_summary(rows, totals):
    print("\n" + "=" * 92)
    print("                    STOCK PORTFOLIO PERFORMANCE")
    print("=" * 92)
    if not rows:
        print("No holdings were entered.")
        return

    print(
        f"{'TICKER':<9}{'SHARES':>9}{'BUY PRICE':>13}{'CURRENT':>13}"
        f"{'MARKET VALUE':>17}{'GAIN / LOSS':>16}{'RETURN':>11}"
    )
    print("-" * 92)

    for row in rows:
        print(
            f"{row['ticker']:<9}{row['shares']:>9.2f}"
            f"${row['buy_price']:>12,.2f}${row['current_price']:>12,.2f}"
            f"${row['market_value']:>16,.2f}${row['gain_loss']:>15,.2f}"
            f"{row['gain_loss_percent']:>9.2f}%"
        )

    print("-" * 92)
    print(f"Total invested:       ${totals['invested']:,.2f}")
    print(f"Current market value: ${totals['market_value']:,.2f}")
    print(f"Total gain/loss:      ${totals['gain_loss']:,.2f}")
    print(f"Total return:         {totals['gain_loss_percent']:.2f}%")
    print("=" * 92)


def save_to_csv(rows, totals):
    timestamp = datetime.now().astimezone().isoformat(timespec="seconds")
    fieldnames = [
        "timestamp", "ticker", "company", "shares", "buy_price",
        "current_price", "invested", "market_value", "gain_loss",
        "gain_loss_percent", "price_source",
    ]

    # One row per holding. Totals are repeated so each row is self-contained.
    file_exists_and_has_data = OUTPUT_FILE.exists() and OUTPUT_FILE.stat().st_size > 0
    with OUTPUT_FILE.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists_and_has_data:
            writer.writeheader()
        for row in rows:
            output_row = {"timestamp": timestamp, **row}
            writer.writerow(output_row)

    print(f"\nPortfolio report saved to: {OUTPUT_FILE.name}")


def main():
    print("=" * 55)
    print("          STOCK PORTFOLIO PERFORMANCE TRACKER")
    print("=" * 55)
    companies = load_companies()
    print(f"Loaded {len(companies)} ticker symbols from {CONSTITUENTS_FILE.name}.")
    print("Note: prices are indicative latest available quotes, not guaranteed real-time.")

    positions = collect_positions(companies)
    if not positions:
        print("\nNo stocks were added. No report was generated.")
        return

    rows, totals = calculate_summary(positions)
    display_summary(rows, totals)
    save_to_csv(rows, totals)


if __name__ == "__main__":
    main()
