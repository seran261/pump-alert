import requests
import time
from config import BTC_DOMINANCE_MAX, ALLOW_BTC_ALWAYS

COINGECKO_GLOBAL = "https://api.coingecko.com/api/v3/global"

_last = 0
_cache = None

def get_btc_dominance():
    global _last, _cache
    if time.time() - _last < 300 and _cache:
        return _cache
    data = requests.get(COINGECKO_GLOBAL, timeout=10).json()
    _cache = data["data"]["market_cap_percentage"]["btc"]
    _last = time.time()
    return _cache

def btc_dominance_ok(symbol, side):
    if symbol.startswith("BTC") and ALLOW_BTC_ALWAYS:
        return True
    if side == "BUY" and get_btc_dominance() > BTC_DOMINANCE_MAX:
        return False
    return True
