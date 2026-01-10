# strategy.py
from indicators import moving_average, volume_spike
from config import (
    MA_PERIOD,
    VOLUME_LOOKBACK,
    VOLUME_MULTIPLIER,
    TAKE_PROFIT_PERCENT,
    STOP_LOSS_PERCENT
)

def detect_trend(df):
    price = df["close"].iloc[-1]
    ma = moving_average(df["close"], MA_PERIOD).iloc[-1]

    if price > ma:
        return "BUY"
    elif price < ma:
        return "SELL"
    return None

def calculate_tp_sl(price, side):
    if side == "BUY":
        tp = price * (1 + TAKE_PROFIT_PERCENT / 100)
        sl = price * (1 - STOP_LOSS_PERCENT / 100)
    else:
        tp = price * (1 - TAKE_PROFIT_PERCENT / 100)
        sl = price * (1 + STOP_LOSS_PERCENT / 100)

    return round(tp, 6), round(sl, 6)

def generate_signal(df):
    direction = detect_trend(df)
    if not direction:
        return None

    if not volume_spike(df["volume"], VOLUME_LOOKBACK, VOLUME_MULTIPLIER):
        return None

    return direction
