from indicators import *

def scalp_signal(df):
    return (
        volume_spike(df, 2.3)
        and atr(df).iloc[-1] > atr(df).rolling(20).mean().iloc[-1] * 1.6
        and abs(df.close.iloc[-1] - df.vwap.iloc[-1]) / df.vwap.iloc[-1] > 0.5
    )

def intraday_signal(df):
    return (
        volume_spike(df, 2.0)
        and atr(df).iloc[-1] > atr(df).rolling(30).mean().iloc[-1] * 1.4
    )

def long_term_signal(df):
    return (
        df.volume.iloc[-1] > df.volume.rolling(50).mean().iloc[-1] * 1.8
        and df.close.iloc[-1] > df.close.rolling(50).mean().iloc[-1]
    )
