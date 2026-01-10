import time
from scanner import top_symbols, scan
from config import *

print("🚀 Crypto Signal Bot Started")

symbols = top_symbols()

while True:
    for s in symbols:
        for tf in SCALP_TF + INTRADAY_TF + LONG_TF:
            try:
                scan(s, tf, "SPOT")
                scan(s, tf, "FUTURES")
            except:
                pass
    time.sleep(SCAN_INTERVAL)
