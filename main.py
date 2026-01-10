# main.py
import threading
import os
from flask import Flask
from scanner import scanner_loop

app = Flask(__name__)

# =========================
# FIXED WHITELIST (BASE ASSETS)
# =========================

WHITELIST = {
    "BTC", "ETH", "USDT", "XRP", "BNB", "SOL", "USDC", "TRX", "DOGE", "ADA",
    "BCH", "LINK", "LTC", "MATIC", "XLM", "AVAX", "SUI", "HBAR", "NEAR",
    "ALGO", "ATOM", "TON", "ICP", "VET", "FIL",
    "APT", "FTM", "ARB", "EOS", "XTZ", "CAKE", "BSV", "IMX", "ZEC",
    "XRD", "BIT", "CRO", "KCS", "MKR",
    "SHIB", "BLAST", "OP", "GALA", "HNT", "RNDR", "QTUM"
}

# Leveraged tokens to exclude
BANNED_SUFFIXES = ("UPUSDT", "DOWNUSDT", "BULLUSDT", "BEARUSDT")


def get_whitelisted_symbols():
    """
    Build Binance USDT symbols ONLY from the fixed whitelist.
    """
    symbols = []

    for base in WHITELIST:
        symbol = f"{base}USDT"

        # Skip leveraged-style symbols defensively
        if symbol.endswith(BANNED_SUFFIXES):
            continue

        symbols.append(symbol)

    return sorted(symbols)


def start_scanner():
    symbols = get_whitelisted_symbols()

    print(f"✅ Scanner started for {len(symbols)} whitelisted symbols")
    print("📌 Symbols:", ", ".join(symbols))

    if not symbols:
        print("❌ Whitelist empty — nothing to scan")
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
