# scanner.py
import time
import requests
import pandas as pd
from strategy import generate_signal, calculate_tp_sl
from telegram import send_signal
from config import TIMEFRAMES, SCAN_INTERVAL

BINANCE_URL = "https://api.binance.com/api/v3/klines"
LAST_SIGNAL = {}  # (symbol, tf) -> BUY/SELL

def fetch_klines(symbol, tf, limit=200):
    r = requests.get(
        BINANCE_URL,
        params={"symbol": symbol, "interval": tf, "limit": limit},
        timeout=10
    )
    data = r.json()

    df = pd.DataFrame(data, columns=[
        "time","open","high","low","close","volume",
        "_","_","_","_","_","_"
    ])

    df["close"] = df["close"].astype(float)
    df["volume"] = df["volume"].astype(float)
    return df

def scan_symbol(symbol):
    for tf in TIMEFRAMES:
        print(f"🔍 Checking {symbol} {tf}")
        df = fetch_klines(symbol, tf)

        direction = generate_signal(df)
        if not direction:
            return

        key = (symbol, tf)
        if LAST_SIGNAL.get(key) == direction:
            return

        LAST_SIGNAL[key] = direction

        entry = df["close"].iloc[-1]
        tp, sl = calculate_tp_sl(entry, direction)

        print(f"🚀 SIGNAL {symbol} {direction} TP:{tp} SL:{sl}")

        send_signal("SPOT", symbol, tf, direction, entry, tp, sl)
        send_signal("FUTURES", symbol, tf, direction, entry, tp, sl)

def scanner_loop(symbols):
    while True:
        print("⏱ Scanner heartbeat...")
        for symbol in symbols:
            try:
                scan_symbol(symbol)
            except Exception as e:
                print(f"❌ {symbol} error: {e}")
        time.sleep(SCAN_INTERVAL)
