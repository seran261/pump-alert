import ccxt, pandas as pd
from config import *
from telegram import send
from indicators import *
from strategy import *

exchange = ccxt.binance({"enableRateLimit": True})

def top_symbols():
    t = exchange.fetch_tickers()
    pairs = [
        s for s in t
        if s.endswith("/USDT") and t[s]["quoteVolume"]
    ]
    pairs.sort(key=lambda x: t[x]["quoteVolume"], reverse=True)
    return pairs[:TOP_COINS]

def scan(symbol, tf, market):
    data = exchange.fetch_ohlcv(symbol, tf, limit=150)
    df = pd.DataFrame(data, columns=["t","open","high","low","close","volume"])
    df["vwap"] = vwap(df)
    delta = delta_ratio(df)

    signal = None

    if tf in SCALP_TF and scalp_signal(df):
        signal = "SCALP"

    elif tf in INTRADAY_TF and intraday_signal(df):
        signal = "INTRADAY"

    elif tf in LONG_TF and long_term_signal(df):
        signal = "LONG TERM"

    if not signal:
        return

    if market == "SPOT":
        side = "BUY"
    else:
        side = "BUY" if delta > DELTA_BULL else "SELL"

    send(
        f"📡 *{signal} SIGNAL*\n"
        f"Market: `{market}`\n"
        f"Symbol: `{symbol}`\n"
        f"TF: `{tf}`\n"
        f"Side: *{side}*\n"
        f"Price: `{df.close.iloc[-1]}`"
    )
