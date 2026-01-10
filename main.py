# main.py
import threading
import os
from flask import Flask
from scanner import scanner_loop

app = Flask(__name__)

SUPPORTED_ASSETS = {
    "BTC","ETH","BNB","SOL","XRP","ADA","DOGE","AVAX","LINK","LTC",
    "MATIC","TRX","XLM","TON","APT","ATOM","ICP","HBAR","NEAR",
    "ARB","OP","FTM","SUI","ALGO","EOS","XTZ","BCH","KAS","INJ",
    "GRT","DASH","CAKE","MKR","SHIB","RNDR","IMX","GALA","HNT"
}

def get_symbols():
    return sorted(f"{a}USDT" for a in SUPPORTED_ASSETS)

def start_scanner():
    symbols = get_symbols()
    print(f"✅ OKX FUTURES scanner started for {len(symbols)} symbols")
    scanner_loop(symbols)

@app.route("/")
def health():
    return "OKX Futures Bot Running", 200

if __name__ == "__main__":
    threading.Thread(target=start_scanner, daemon=True).start()
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
