# main.py
import asyncio
import threading
import os
from flask import Flask
import aiohttp
from scanner import scanner_loop

app = Flask(__name__)

# =========================
# API ENDPOINTS
# =========================

COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/markets"
BINANCE_EXCHANGE_URL = "https://api.binance.com/api/v3/exchangeInfo"


# =========================
# ASYNC HELPERS
# =========================

async def fetch_json(session, url, params=None):
    async with session.get(url, params=params, timeout=20) as resp:
        return await resp.json()


async def get_top_50_by_market_cap_async():
    """
    1. Fetch TOP 50 coins by market cap from CoinGecko
    2. Fetch Binance exchange symbols
    3. Map CoinGecko coins → Binance USDT pairs
    """

    async with aiohttp.ClientSession() as session:
        # Run both API calls in parallel
        coingecko_task = fetch_json(
            session,
            COINGECKO_URL,
            {
                "vs_currency": "usd",
                "order": "market_cap_desc",
                "per_page": 50,   # ✅ TOP 50 ONLY
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

    # Exclude leveraged tokens
    banned_suffixes = (
        "UPUSDT",
        "DOWNUSDT",
        "BULLUSDT",
        "BEARUSDT"
    )

    resolved_symbols = []

    for s in binance_data["symbols"]:
        symbol = s["symbol"]
        base_asset = s["baseAsset"]

        # Only USDT pairs
        if not symbol.endswith("USDT"):
            continue

        # Skip leveraged tokens
        if symbol.endswith(banned_suffixes):
            continue

        # Match CoinGecko symbol with Binance base asset
        if base_asset in top_symbols:
            resolved_symbols.append(symbol)

    return resolved_symbols


# =========================
# SCANNER STARTER
# =========================

def start_scanner():
    symbols = asyncio.run(get_top_50_by_market_cap_async())

    print(f"✅ Scanner started for {len(symbols)} symbols (Top 50 Market Cap • Async)")

    if not symbols:
        print("❌ No symbols resolved — check CoinGecko / Binance mapping")
        return

    scanner_loop(symbols)


# =========================
# HEALTH CHECK
# =========================

@app.route("/")
def health():
    return "Bot is running", 200


# =========================
# ENTRY POINT
# =========================

if __name__ == "__main__":
    # Start scanner in background thread
    threading.Thread(
        target=start_scanner,
        daemon=True
    ).start()

    # Railway-required port binding
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
