import pandas as pd
import numpy as np

def vwap(df):
    return (df.close * df.volume).cumsum() / df.volume.cumsum()

def atr(df, period=14):
    tr = pd.concat([
        df.high - df.low,
        abs(df.high - df.close.shift()),
        abs(df.low - df.close.shift())
    ], axis=1).max(axis=1)
    return tr.rolling(period).mean()

def volume_spike(df, mult):
    return df.volume.iloc[-1] > df.volume.rolling(20).mean().iloc[-1] * mult

def delta_ratio(df):
    delta = df.close - df.open
    bull = delta[delta > 0].sum()
    bear = abs(delta[delta < 0].sum())
    return bull / (bull + bear) if bull + bear else 0.5
