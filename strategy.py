# strategy.py
from indicators import moving_average, volume_spike
from config import MA_PERIOD

def detect_trend(df):
    ma = moving_average(df["close"], MA_PERIOD).iloc[-1]
    price = df["close"].iloc[-1]

    if price > ma:
        return "BUY"
    elif price < ma:
        return "SELL"
    return None

def long_term_signal(df):
    direction = detect_trend(df)
    if not direction:
        return None

    if not volume_spike(df["volume"]):
        return None

    return direction
