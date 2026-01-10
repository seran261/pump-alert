# strategy.py
from indicators import (
    moving_average,
    volume_spike,
    breakout_high,
    breakout_low,
    atr
)
from config import *

def detect_trend(df):
    if len(df) < MA_PERIOD:
        return None
    price = df["close"].iloc[-1]
    ma = moving_average(df["close"], MA_PERIOD).iloc[-1]
    if price > ma:
        return "BUY"
    elif price < ma:
        return "SELL"
    return None

def calculate_atr_sl_tp(price, atr_value, side):
    if side == "BUY":
        sl = price - atr_value * ATR_SL_MULTIPLIER
        tp = price + atr_value * ATR_TP_MULTIPLIER
    else:
        sl = price + atr_value * ATR_SL_MULTIPLIER
        tp = price - atr_value * ATR_TP_MULTIPLIER
    return round(tp, 6), round(sl, 6)

def signal_confidence(trend, vol_ok, breakout_ok, atr_ok):
    score = 0
    if trend:
        score += WEIGHT_TREND
    if vol_ok:
        score += WEIGHT_VOLUME
    if breakout_ok:
        score += WEIGHT_BREAKOUT
    if atr_ok:
        score += WEIGHT_ATR
    return score

def generate_signal(df):
    if len(df) < max(MA_PERIOD, ATR_PERIOD, BREAKOUT_LOOKBACK):
        return None

    trend = detect_trend(df)
    if not trend:
        return None

    vol_ok = volume_spike(df["volume"], VOLUME_LOOKBACK, VOLUME_MULTIPLIER)

    breakout_ok = (
        breakout_high(df, BREAKOUT_LOOKBACK)
        if trend == "BUY"
        else breakout_low(df, BREAKOUT_LOOKBACK)
    )

    # 🔑 Volume OR Breakout logic
    if not (vol_ok or breakout_ok):
        return None

    atr_val = atr(df, ATR_PERIOD).iloc[-1]
    atr_ok = atr_val > atr(df, ATR_PERIOD).mean().iloc[-1]

    confidence = signal_confidence(trend, vol_ok, breakout_ok, atr_ok)

    if confidence < MIN_CONFIDENCE_SCORE:
        return None

    return {
        "side": trend,
        "confidence": confidence,
        "atr": atr_val
    }
