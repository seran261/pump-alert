# main.py
import threading
import os
from flask import Flask
from scanner import scanner_loop

app = Flask(__name__)

# ======================================================
# SUPPORTED BASE ASSETS (BINANCE USDT WILL BE USED)
# ======================================================

SUPPORTED_ASSETS = {
    # Major L1 / L0
    "BTC", "ETH", "USDT", "XRP", "BNB", "SOL", "USDC", "ADA", "DOGE", "MATIC",
    "TRX", "AVAX", "LINK", "LTC", "XLM", "TON", "APT", "ATOM", "VET", "ICP",
    "HBAR", "NEAR", "FTM", "ARB", "OP", "SUI", "ALGO", "EOS", "XTZ", "BCH",
    "XRD", "KCS", "CRO", "MKR", "BSV", "BIT", "ZEC", "SHIB", "RNDR", "IMX",
    "GALA", "HNT", "FLOW", "BLAST", "AR", "STX", "AXS", "TIA", "MNT",
    "DYDX", "INJ", "KAS", "GRT", "DASH", "NEXO", "SUSHI", "CHZ", "CELO",
    "GT", "AURORA", "CAKE", "CVX", "AGIX", "SNX", "DCR", "OMG", "BTG",
    "ONE", "BAL", "BAT", "SC", "BNT", "GNO", "QNT", "ICX", "HOT", "FET",
    "XEM", "BAKE", "REEF", "XVG", "THETA", "AMP", "ARDR", "NANO", "ANKR",
    "KSM", "WON", "RSR", "OXT", "EWT", "STORJ", "SNT"
}

# ======================================================
# ASSET ALIASES / VARIANTS
# (maps multiple names → single Binance base asset)
# ======================================================

ALIASES = {
    "STETH": "ETH",      # Lido Staked ETH → ETH
    "INT": None,         # Not on Binance
    "EOSNEW": "EOS",     # EOS Network (New)
    "APTOSWAP": "APT",   # Aptos variants
    "TONN": "TON",       # Tokamak / Ton variants
    "HELIUM": "HNT",     # Helium variants
    "ARBNOVA": "ARB"     # Arbitrum Nova
}

# ======================================================
# LEVERAGED TOKENS TO EXCLUDE
# ======================================================

BANNED_SUFFIXES = ("UPUSDT", "DOWNUSDT", "BULLUSDT", "BEARUSDT")


def normalize_asset(asset):
    """
    Normalize asset using alias table.
    Returns None if asset should be ignored.
    """
    asset = asset.upper()

    if asset in ALIASES:
        return ALIASES[asset]

    return asset


def get_supported_symbols():
    """
    Build Binance USDT symbols from supported asset list.
    Non-listed pairs will be skipped later by scanner safely.
    """
    symbols = []

    for asset in SUPPORTED_ASSETS:
        base = normalize_asset(asset)
        if not base:
            continue

        symbol = f"{base}USDT"

        if symbol.endswith(BANNED_SUFFIXES):
            continue

        symbols.append(symbol)

    return sorted(set(symbols))


def start_scanner():
    symbols = get_supported_symbols()

    print(f"✅ Scanner started for {len(symbols)} supported symbols")
    print("📌 Symbols:", ", ".join(symbols))

    if not symbols:
        print("❌ No valid symbols to scan")
        return

    scanner_loop(symbols)


# ======================================================
# HEALTH CHECK
# ======================================================

@app.route("/")
def health():
    return "Bot is running", 200


# ======================================================
# ENTRY POINT
# ======================================================

if __name__ == "__main__":
    threading.Thread(
        target=start_scanner,
        daemon=True
    ).start()

    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
