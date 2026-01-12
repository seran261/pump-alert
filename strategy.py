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
    return "BUY" if price > ma else "SELL"

def calculate_multi_tp(entry, atr_val, side):
    if side == "BUY":
        tp1 = entry + atr_val * TP1_ATR
        tp2 = entry + atr_val * TP2_ATR
        tp3 = entry + atr_val * TP3_ATR
        sl = entry - atr_val * ATR_SL_MULTIPLIER
    else:
        tp1 = entry - atr_val * TP1_ATR
        tp2 = entry - atr_val * TP2_ATR
        tp3 = entry - atr_val * TP3_ATR
        sl = entry + atr_val * ATR_SL_MULTIPLIER

    return {
        "tp1": round(tp1, 6),
        "tp2": round(tp2, 6),
        "tp3": round(tp3, 6),
        "sl": round(sl, 6)
    }

def confidence_score(trend_ltf, trend_htf, vol_ok, breakout_ok, atr_ok):
    score = 0
    if trend_ltf:
        score += WEIGHT_TREND_LTF
    if trend_htf and trend_ltf == trend_htf:
        score += WEIGHT_TREND_HTF
    if vol_ok:
        score += WEIGHT_VOLUME
    if breakout_ok:
        score += WEIGHT_BREAKOUT
    if atr_ok:
        score += WEIGHT_ATR
    return score

def generate_signal(df_ltf, df_htf):
    min_len = max(MA_PERIOD, ATR_PERIOD, BREAKOUT_LOOKBACK, VOLUME_LOOKBACK)
    if len(df_ltf) < min_len or len(df_htf) < min_len:
        return None

    trend_ltf = detect_trend(df_ltf)
    trend_htf = detect_trend(df_htf)

    # ❌ Reject if HTF disagrees
    if trend_ltf != trend_htf:
        return None

    vol_ok = volume_spike(
        df_ltf["volume"],
        VOLUME_LOOKBACK,
        VOLUME_MULTIPLIER
    )

    breakout_ok = (
        breakout_high(df_ltf, BREAKOUT_LOOKBACK)
        if trend_ltf == "BUY"
        else breakout_low(df_ltf, BREAKOUT_LOOKBACK)
    )

    # Volume OR Breakout
    if not (vol_ok or breakout_ok):
        return None

    atr_series = atr(df_ltf, ATR_PERIOD)
    if atr_series.isna().all():
        return None

    atr_val = atr_series.iloc[-1]
    atr_ok = atr_val > atr_series.mean()

    score = confidence_score(
        trend_ltf,
        trend_htf,
        vol_ok,
        breakout_ok,
        atr_ok
    )

    if score < MIN_CONFIDENCE_SCORE:
        return None

    return {
        "side": trend_ltf,
        "atr": atr_val,
        "confidence": score
    }
