# main.py
import threading
import os
import requests
from flask import Flask
from scanner import scanner_loop

app = Flask(__name__)

COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/markets"
BINANCE_SYMBOL_URL = "https://api.binance.com/api/v3/exchangeInfo"


def get_top_100_by_market_cap():
    """
    1. Fetch top 100 coins by market cap from CoinGecko
    2. Map them to Binance USDT symbols
    3. Filter leveraged tokens
    """

    # 1️⃣ Get top 100 coins by market cap
    cg_params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 100,
        "page": 1
    }

    coins = requests.get(
        COINGECKO_URL,
        params=cg_params,
        timeout=15
    ).json()

    # Extract symbols (lowercase from CoinGecko)
    top_symbols = {c["symbol"].upper() for c in coins}

    # 2️⃣ Fetch Binance exchange symbols
    exchange_info = requests.get(
        BINANCE_SYMBOL_URL,
        timeout=15
    ).json()

    banned_suffixes = ("UPUSDT", "DOWNUSDT", "BULLUSDT", "BEARUSDT")

    binance_symbols = []

    for s in exchange_info["symbols"]:
        symbol = s["symbol"]

        if not symbol.endswith("USDT"):
            continue

        if symbol.endswith(banned_suffixes):
            continue

        base_asset = s["baseAsset"]

        # 3️⃣ Match CoinGecko symbol with Binance base asset
        if base_asset in top_symbols:
            binance_symbols.append(symbol)

    return binance_symbols


def start_scanner():
    symbols = get_top_100_by_market_cap()

    print(f"✅ Scanner started for {len(symbols)} symbols (Top 100 Market Cap)")

    if not symbols:
        print("❌ No symbols resolved from CoinGecko → Binance mapping")
        return

    scanner_loop(symbols)


@app.route("/")
def health():
    return "Bot is running", 200


if __name__ == "__main__":
    threading.Thread(
        target=start_scanner,
        daemon=True
    ).start()

    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
