import time
import asyncio
import aiohttp
import pandas as pd
from strategy import generate_signal, calculate_multi_tp
from telegram import send_signal
from config import LOWER_TF, HIGHER_TF, SCAN_INTERVAL
from dominance import btc_dominance_ok

BINANCE_URL = "https://api.binance.com/api/v3/klines"
LAST_SIGNAL = {}

# -------------------------
# ASYNC FETCH
# -------------------------

async def fetch_klines(session, symbol, tf, limit=200):
    params = {
        "symbol": symbol,
        "interval": tf,
        "limit": limit
    }
    async with session.get(BINANCE_URL, params=params, timeout=10) as resp:
        data = await resp.json()

    if not isinstance(data, list) or len(data) < 60:
        return None

    df = pd.DataFrame(data, columns=[
        "time","open","high","low","close","volume",
        "_","_","_","_","_","_"
    ])

    for c in ["open","high","low","close","volume"]:
        df[c] = df[c].astype(float)

    return df


async def scan_symbol_async(session, symbol):
    # Fetch LTF & HTF in parallel
    df_ltf, df_htf = await asyncio.gather(
        fetch_klines(session, symbol, LOWER_TF),
        fetch_klines(session, symbol, HIGHER_TF)
    )

    if df_ltf is None or df_htf is None:
        return

    signal = generate_signal(df_ltf, df_htf)
    if not signal:
        return

    # 🧠 BTC DOMINANCE FILTER
    if not btc_dominance_ok(symbol, signal["side"]):
        print(f"🧠 BTC dominance blocks {symbol}")
        return

    key = (symbol, signal["side"])
    if LAST_SIGNAL.get(key):
        return

    LAST_SIGNAL[key] = True

    entry = df_ltf["close"].iloc[-1]
    levels = calculate_multi_tp(entry, signal["atr"], signal["side"])

    send_signal(
        symbol=symbol,
        tf=f"{LOWER_TF} → {HIGHER_TF}",
        side=signal["side"],
        entry=entry,
        sl=levels["sl"],
        tp1=levels["tp1"],
        tp2=levels["tp2"],
        tp3=levels["tp3"],
        confidence=signal["confidence"]
    )


async def scanner_async(symbols):
    async with aiohttp.ClientSession() as session:
        tasks = [scan_symbol_async(session, s) for s in symbols]
        await asyncio.gather(*tasks)


def scanner_loop(symbols):
    while True:
        print("⚡ Async scanner heartbeat...")
        asyncio.run(scanner_async(symbols))
        time.sleep(SCAN_INTERVAL)
