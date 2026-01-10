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

# Stablecoins to EXCLUDE
STABLECOINS = {
    "USDT", "USDC", "BUSD", "DAI", "TUSD",
    "USDP", "USDS", "FDUSD", "FRAX"
}


# =========================
# ASYNC HELPERS
# =========================

async def fetch_json(session, url, params=None):
    async with session.get(url, params=params, timeout=20) as resp:
        return await resp.json()


async def get_top_50_by_market_cap_async():
    """
    ✔ Fetch TOP 50 coins by market cap from CoinGecko
    ✔ Exclude stablecoins
    ✔ Map to Binance USDT pairs safely
    """

    async with aiohttp.ClientSession() as session:
        coingecko_task = fetch_json(
            session,
            COINGECKO_URL,
            {
                "vs_currency": "usd",
                "order": "market_cap_desc",
                "per_page": 100,  # fetch extra to allow filtering
                "page": 1
            }
        )

        binance_task = fetch_json(session, BINANCE_EXCHANGE_URL)

        coingecko_data, binance_data = await asyncio.gather(
            coingecko_task,
            binance_task
        )

    # 1️⃣ Extract VALID base assets from CoinGecko
    valid_assets = []
    for coin in coingecko_data:
        symbol = coin["symbol"].upper()

        # ❌ skip stablecoins
        if symbol in STABLECOINS:
            continue

        valid_assets.append(symbol)

        if len(valid_assets) >= 50:
            break

    # 2️⃣ Map to Binance USDT pairs
    banned_suffixes = ("UPUSDT", "DOWNUSDT", "BULLUSDT", "BEARUSDT")

    resolved_symbols = []

    for s in binance_data["symbols"]:
        symbol = s["symbol"]
        base_asset = s["baseAsset"]

        if not symbol.endswith("USDT"):
            continue

        if symbol.endswith(banned_suffixes):
            continue

        if base_asset in valid_assets:
            resolved_symbols.append(symbol)

    return resolved_symbols


# =========================
# SCANNER STARTER
# =========================

def start_scanner():
    symbols = asyncio.run(get_top_50_by_market_cap_async())

    print(
        f"✅ Scanner started for {len(symbols)} symbols "
        f"(Top 50 Market Cap • Stablecoins Removed)"
    )

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
    threading.Thread(
        target=start_scanner,
        daemon=True
    ).start()

    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
