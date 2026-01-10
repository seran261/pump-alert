import requests
import time
from config import BTC_DOMINANCE_MAX, ALLOW_BTC_ALWAYS

COINGECKO_GLOBAL = "https://api.coingecko.com/api/v3/global"

_last_fetch = 0
_cached_dominance = None


def get_btc_dominance():
    global _last_fetch, _cached_dominance

    if time.time() - _last_fetch < 300 and _cached_dominance:
        return _cached_dominance

    data = requests.get(COINGECKO_GLOBAL, timeout=10).json()
    dominance = data["data"]["market_cap_percentage"]["btc"]

    _cached_dominance = dominance
    _last_fetch = time.time()
    return dominance


def btc_dominance_ok(symbol, side):
    dominance = get_btc_dominance()

    # Always allow BTC trades
    if symbol.startswith("BTC") and ALLOW_BTC_ALWAYS:
        return True

    # Block ALT BUY in high BTC dominance
    if side == "BUY" and dominance > BTC_DOMINANCE_MAX:
        return False

    return True
