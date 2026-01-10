# main.py
import threading
import os
from flask import Flask
from scanner import scanner_loop

app = Flask(__name__)

SUPPORTED_ASSETS = {
    "BTC", "ETH", "XRP", "BNB", "SOL", "USDC", "ADA", "DOGE", "MATIC",
    "TRX", "AVAX", "LINK", "LTC", "XLM", "TON", "APT", "ATOM", "VET",
    "ICP", "HBAR", "NEAR", "FTM", "ARB", "OP", "SUI", "ALGO", "EOS",
    "XTZ", "BCH", "XRD", "KCS", "CRO", "MKR", "BSV", "BIT", "ZEC",
    "SHIB", "RNDR", "IMX", "GALA", "HNT", "FLOW", "BLAST", "AR",
    "STX", "AXS", "TIA", "MNT", "DYDX", "INJ", "KAS", "GRT",
    "DASH", "NEXO", "SUSHI", "CHZ", "CELO", "GT", "AURORA",
    "CAKE", "CVX", "AGIX", "SNX", "DCR", "OMG", "BTG", "ONE",
    "BAL", "BAT", "SC", "BNT", "GNO", "QNT", "ICX", "HOT",
    "FET", "XEM", "BAKE", "REEF", "XVG", "THETA", "AMP",
    "ARDR", "NANO", "ANKR", "KSM", "WON", "RSR", "OXT",
    "EWT", "STORJ", "SNT"
}

BLOCKED_BASES = {"USDT", "DAI", "BUSD", "TUSD", "USDP", "FDUSD"}

def get_symbols():
    symbols = []
    for asset in SUPPORTED_ASSETS:
        if asset in BLOCKED_BASES:
            continue
        symbols.append(f"{asset}USDT")
    return sorted(set(symbols))


def start_scanner():
    symbols = get_symbols()
    print(f"✅ OKX scanner started for {len(symbols)} symbols")
    scanner_loop(symbols)


@app.route("/")
def health():
    return "Bot running (OKX)", 200


if __name__ == "__main__":
    threading.Thread(target=start_scanner, daemon=True).start()
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
