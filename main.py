# main.py
import threading
import time
import os
from scanner import scanner_loop
import requests
from flask import Flask

app = Flask(__name__)

def get_top_symbols(limit=200):
    url = "https://api.binance.com/api/v3/ticker/24hr"
    data = requests.get(url, timeout=10).json()

    return [
        d["symbol"] for d in data
        if d["symbol"].endswith("USDT")
    ][:limit]

def start_scanner():
    symbols = get_top_symbols()
    print(f"✅ Scanner started for {len(symbols)} symbols")
    scanner_loop(symbols)

@app.route("/")
def health():
    return "Bot is running", 200

if __name__ == "__main__":
    # start scanner in background
    threading.Thread(target=start_scanner, daemon=True).start()

    # Railway port binding
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
