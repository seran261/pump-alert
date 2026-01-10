import time
import asyncio
import aiohttp
import pandas as pd
from strategy import generate_signal, calculate_multi_tp
from telegram import send_signal
from dominance import btc_dominance_ok
from config import LOWER_TF, HIGHER_TF, SCAN_INTERVAL, MARKET_TYPE

OKX_URL = "https://www.okx.com/api/v5/market/candles"
LAST_SIGNAL = {}

def okx_inst_id(symbol):
    """
    BTCUSDT → BTC-USDT-SWAP (FUTURES)
    BTCUSDT → BTC-USDT (SPOT)
    """
    base = symbol.replace("USDT", "")
    return f"{base}-USDT-SWAP" if MARKET_TYPE == "FUTURES" else f"{base}-USDT"


async def fetch_klines(session, inst_id, tf, limit=200):
    params = {"instId": inst_id, "bar": tf, "limit": limit}

    async with session.get(OKX_URL, params=params, timeout=10) as resp:
        data = await resp.json()

    if "data" not in data or len(data["data"]) < 60:
        return None

    df = pd.DataFrame(
        data["data"],
        columns=[
            "ts","open","high","low",
            "close","volume","volCcy","volQuote","confirm"
        ]
    )

    df = df.iloc[::-1]

    for c in ["open","high","low","close","volume"]:
        df[c] = df[c].astype(float)

    return df


async def scan_symbol_async(session, symbol):
    inst = okx_inst_id(symbol)

    df_ltf, df_htf = await asyncio.gather(
        fetch_klines(session, inst, LOWER_TF),
        fetch_klines(session, inst, HIGHER_TF)
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
        symbol=inst,
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
        print("⚡ OKX FUTURES scanner heartbeat...")
        asyncio.run(scanner_async(symbols))
        time.sleep(SCAN_INTERVAL)
