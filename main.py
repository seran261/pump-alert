# main.py
import asyncio
import threading
import os
from flask import Flask
from scanner import scanner_loop
import aiohttp

app = Flask(__name__)

COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/markets"
BINANCE_EXCHANGE_URL = "https://api.binance.com/api/v3/exchangeInfo"


async def fetch_json(session, url, params=None):
    async with session.get(url, params=params, timeout=20) as resp:
        return await resp.json()


async def get_top_100_by_market_cap_async():
    """
    Async:
    1. Fetch top 100 coins by market cap from CoinGecko
    2. Fetch Binance exchange symbols
    3. Map CoinGecko coins → Binance USDT pairs
    """

    async with aiohttp.ClientSession() as session:
        # Run both requests in parallel
        coingecko_task = fetch_json(
            session,
            COINGECKO_URL,
            {
                "vs_currency": "usd",
                "order": "market_cap_desc",
                "per_page": 100,
                "page": 1
            }
        )

        binance_task = fetch_json(session, BINANCE_EXCHANGE_URL)

        coingecko_data, binance_data = await asyncio.gather(
            coingecko_task,
            binance_task
        )

    # Extract CoinGecko symbols (uppercase)
    top_symbols = {coin["symbol"].upper() for coin in coingecko_data}

    banned_suffixes = ("UPUSDT", "DOWNUSDT", "BULLUSDT", "BEARUSDT")

    resolved_symbols = []

    for s in binance_data["symbols"]:
        symbol = s["symbol"]
        base_asset = s["baseAsset"]

        if not symbol.endswith("USDT"):
            continue

        if symbol.endswith(banned_suffixes):
            continue

        if base_asset in top_symbols:
            resolved_symbols.append(symbol)

    return resolved_symbols


def start_scanner():
    # Run async resolver inside thread
    symbols = asyncio.run(get_top_100_by_market_cap_async())

    print(f"✅ Scanner started for {len(symbols)} symbols (Top 100 Market Cap • Async)")

    if not symbols:
        print("❌ No symbols resolved — check CoinGecko / Binance mapping")
        return

    scanner_loop(symbols)


@app.route("/")
def health():
    return "Bot is running", 200


if __name__ == "__main__":
    # Start scanner in background
    threading.Thread(
        target=start_scanner,
        daemon=True
    ).start()

    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
