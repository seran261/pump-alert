# scanner.py
import time
import requests
import pandas as pd
from strategy import long_term_signal
from telegram import send_signal
from config import BINANCE_BASE_URL, TIMEFRAMES, SCAN_INTERVAL

LAST_SIGNAL = {}  # (symbol, timeframe) → direction

def fetch_klines(symbol, interval, limit=200):
    url = f"{BINANCE_BASE_URL}/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    data = requests.get(url, params=params).json()

    df = pd.DataFrame(data, columns=[
        "time","open","high","low","close","volume",
        "_","_","_","_","_","_"
    ])

    df["close"] = df["close"].astype(float)
    df["volume"] = df["volume"].astype(float)
    return df

def scan_symbol(symbol):
    for tf in TIMEFRAMES:
        df = fetch_klines(symbol, tf)
        direction = long_term_signal(df)
        if not direction:
            continue

        key = (symbol, tf)

        # 🚫 BLOCK opposite or duplicate signals
        if key in LAST_SIGNAL and LAST_SIGNAL[key] == direction:
            continue

        LAST_SIGNAL[key] = direction

        price = df["close"].iloc[-1]

        # ✅ SAME direction used for SPOT & FUTURES
        send_signal("SPOT", symbol, tf, direction, price)
        send_signal("FUTURES", symbol, tf, direction, price)

def scanner_loop(symbols):
    while True:
        for symbol in symbols:
            try:
                scan_symbol(symbol)
            except Exception as e:
                print(f"Error {symbol}: {e}")
        time.sleep(SCAN_INTERVAL)
