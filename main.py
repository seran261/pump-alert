# main.py
import threading
import os
import requests
from flask import Flask
from scanner import scanner_loop
from config import SYMBOL_LIMIT

app = Flask(__name__)

def get_symbols():
    data = requests.get(
        "https://api.binance.com/api/v3/ticker/24hr",
        timeout=10
    ).json()

    return [
        d["symbol"] for d in data
        if d["symbol"].endswith("USDT")
    ][:SYMBOL_LIMIT]

def start_scanner():
    symbols = get_symbols()
    print(f"✅ Scanner started for {len(symbols)} symbols")
    scanner_loop(symbols)

@app.route("/")
def health():
    return "Bot is running", 200

if __name__ == "__main__":
    threading.Thread(target=start_scanner, daemon=True).start()
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
