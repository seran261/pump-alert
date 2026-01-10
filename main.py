# main.py
from scanner import scanner_loop
import requests

def get_top_symbols(limit=200):
    url = "https://api.binance.com/api/v3/ticker/24hr"
    data = requests.get(url).json()

    usdt_pairs = [
        d["symbol"] for d in data
        if d["symbol"].endswith("USDT")
    ]
    return usdt_pairs[:limit]

if __name__ == "__main__":
    symbols = get_top_symbols()
    scanner_loop(symbols)
