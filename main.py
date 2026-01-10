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

    banned = ("UP","DOWN","BULL","BEAR","USD","EUR","GBP")
    symbols = []

    for d in data:
        s = d["symbol"]
        if s.endswith("USDT") and not any(b in s for b in banned):
            symbols.append(s)

    return symbols[:SYMBOL_LIMIT]

def start_scanner():
    symbols = get_symbols()
    print(f"✅ Scanner started for {len(symbols)} symbols")
    scanner_loop(symbols)

@app.route("/")
def health():
    return "Bot running", 200

if __name__ == "__main__":
    threading.Thread(target=start_scanner, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
