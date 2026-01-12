# main.py
import asyncio
import threading
import os
import aiohttp
from flask import Flask
from scanner import scanner_loop

app = Flask(__name__)

COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/markets"
BYBIT_SYMBOLS_URL = "https://api.bybit.com/v5/market/instruments-info"

STABLES = {
    "USDT","USDC","DAI","BUSD","TUSD","USDP","FDUSD","USDS"
}

async def fetch_json(session, url, params=None):
    async with session.get(url, params=params, timeout=20) as r:
        return await r.json()


async def get_top_100_bybit_futures():
    """
    1. Fetch Top 100 coins by market cap (CoinGecko)
    2. Fetch Bybit USDT perpetual symbols
    3. Keep intersection
    """
    async with aiohttp.ClientSession() as session:
        cg_task = fetch_json(
            session,
            COINGECKO_URL,
            {
                "vs_currency": "usd",
                "order": "market_cap_desc",
                "per_page": 120,
                "page": 1
            }
        )

        bybit_task = fetch_json(
            session,
            BYBIT_SYMBOLS_URL,
            {
                "category": "linear",
                "limit": 1000
            }
        )

        cg_data, bybit_data = await asyncio.gather(cg_task, bybit_task)

    # Top assets by market cap
    top_assets = []
    for c in cg_data:
        sym = c["symbol"].upper()
        if sym in STABLES:
            continue
        top_assets.append(sym)
        if len(top_assets) >= 100:
            break

    # Bybit USDT perpetual base assets
    bybit_bases = {
        i["symbol"].replace("USDT", "")
        for i in bybit_data["result"]["list"]
        if i["symbol"].endswith("USDT")
    }

    symbols = []
    for asset in top_assets:
        if asset in bybit_bases:
            symbols.append(f"{asset}USDT")

    return sorted(symbols)


def start_scanner():
    symbols = asyncio.run(get_top_100_bybit_futures())

    print(f"✅ BYBIT FUTURES scanner started for {len(symbols)} TOP-100 symbols")
    print("📌 Symbols:", ", ".join(symbols))

    if not symbols:
        print("❌ No Bybit futures symbols resolved")
        return

    scanner_loop(symbols)


@app.route("/")
def health():
    return "Bybit Futures Bot Running", 200


if __name__ == "__main__":
    threading.Thread(target=start_scanner, daemon=True).start()
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
