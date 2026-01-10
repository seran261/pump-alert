# main.py
import threading
import os
import requests
from flask import Flask
from scanner import scanner_loop
from config import SYMBOL_LIMIT

app = Flask(__name__)

def get_symbols():
    """
    Fetch top USDT symbols from Binance
    and exclude ONLY leveraged tokens.
    """
    url = "https://api.binance.com/api/v3/ticker/24hr"
    data = requests.get(url, timeout=10).json()

    # 🚫 Exclude leveraged tokens ONLY
    banned_suffixes = (
        "UPUSDT",
        "DOWNUSDT",
        "BULLUSDT",
        "BEARUSDT"
    )

    symbols = []
    for d in data:
        symbol = d.get("symbol")

        if not symbol:
            continue

        # ✅ Only USDT pairs
        if not symbol.endswith("USDT"):
            continue

        # 🚫 Skip leveraged tokens
        if symbol.endswith(banned_suffixes):
            continue

        symbols.append(symbol)

    return symbols[:SYMBOL_LIMIT]

def start_scanner():
    symbols = get_symbols()

    print(f"✅ Scanner started for {len(symbols)} symbols")

    if not symbols:
        print("❌ No symbols found — check filter logic")
        return

    scanner_loop(symbols)

@app.route("/")
def health():
    return "Bot is running", 200

if __name__ == "__main__":
    # Start scanner in background thread
    threading.Thread(
        target=start_scanner,
        daemon=True
    ).start()

    # Railway-required port binding
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
