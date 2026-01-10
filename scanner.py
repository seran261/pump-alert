import time
import requests
import pandas as pd
from strategy import generate_signal, calculate_atr_sl_tp
from telegram import send_signal
from config import TIMEFRAMES, SCAN_INTERVAL

BINANCE_URL = "https://api.binance.com/api/v3/klines"
LAST_SIGNAL = {}

def fetch_klines(symbol, tf, limit=200):
    r = requests.get(
        BINANCE_URL,
        params={"symbol": symbol, "interval": tf, "limit": limit},
        timeout=10
    )
    data = r.json()

    if not isinstance(data, list) or len(data) < 60:
        return None

    df = pd.DataFrame(data, columns=[
        "time","open","high","low","close","volume",
        "_","_","_","_","_","_"
    ])

    for col in ["open","high","low","close","volume"]:
        df[col] = df[col].astype(float)

    return df

def scan_symbol(symbol):
    for tf in TIMEFRAMES:
        df = fetch_klines(symbol, tf)
        if df is None or df.empty:
            return

        signal = generate_signal(df)
        if not signal:
            return

        key = (symbol, tf)
        if LAST_SIGNAL.get(key) == signal["side"]:
            return

        LAST_SIGNAL[key] = signal["side"]

        entry = df["close"].iloc[-1]
        tp, sl = calculate_atr_sl_tp(
            entry,
            signal["atr"],
            signal["side"]
        )

        print(
            f"🚀 SIGNAL {symbol} {signal['side']} "
            f"TP:{tp} SL:{sl} CONF:{signal['confidence']}"
        )

        send_signal(
            symbol=symbol,
            tf=tf,
            side=signal["side"],
            entry=entry,
            tp=tp,
            sl=sl,
            confidence=signal["confidence"]
        )

def scanner_loop(symbols):
    while True:
        print("⏱ Scanner heartbeat...")
        for symbol in symbols:
            try:
                scan_symbol(symbol)
            except Exception as e:
                print(f"❌ {symbol}: {e}")
        time.sleep(SCAN_INTERVAL)
