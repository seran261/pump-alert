import time
import asyncio
import aiohttp
import pandas as pd
from strategy import generate_signal, calculate_multi_tp
from telegram import send_signal
from dominance import btc_dominance_ok
from config import LOWER_TF, HIGHER_TF, SCAN_INTERVAL

BYBIT_KLINE_URL = "https://api.bybit.com/v5/market/kline"
LAST_SIGNAL = {}

async def fetch_klines(session, symbol, interval, limit=200):
    params = {
        "category": "linear",
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }

    async with session.get(BYBIT_KLINE_URL, params=params, timeout=10) as r:
        j = await r.json()

    if j.get("retCode") != 0 or not j["result"]["list"]:
        return None

    data = j["result"]["list"]
    if len(data) < 60:
        return None

    df = pd.DataFrame(
        data,
        columns=["ts","open","high","low","close","volume","turnover"]
    )

    df = df.iloc[::-1]

    for c in ["open","high","low","close","volume"]:
        df[c] = df[c].astype(float)

    return df


async def scan_symbol_async(session, symbol):
    df_ltf, df_htf = await asyncio.gather(
        fetch_klines(session, symbol, LOWER_TF),
        fetch_klines(session, symbol, HIGHER_TF)
    )

    if df_ltf is None or df_htf is None:
        return

    signal = generate_signal(df_ltf, df_htf)
    if not signal:
        return

    if not btc_dominance_ok(symbol, signal["side"]):
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
        await asyncio.gather(
            *(scan_symbol_async(session, s) for s in symbols)
        )


def scanner_loop(symbols):
    while True:
        print("⚡ BYBIT FUTURES TOP-100 scanner heartbeat...")
        asyncio.run(scanner_async(symbols))
        time.sleep(SCAN_INTERVAL)
