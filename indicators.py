# indicators.py
import pandas as pd

def moving_average(series, period):
    return series.rolling(period).mean()

def true_range(df):
    high_low = df["high"] - df["low"]
    high_close = (df["high"] - df["close"].shift()).abs()
    low_close = (df["low"] - df["close"].shift()).abs()
    return pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)

def atr(df, period):
    tr = true_range(df)
    return tr.rolling(period).mean()

def volume_spike(volume, lookback, multiplier):
    avg = volume.rolling(lookback).mean()
    return volume.iloc[-1] > avg.iloc[-1] * multiplier

def breakout_high(df, lookback):
    return df["close"].iloc[-1] > df["high"].rolling(lookback).max().iloc[-2]

def breakout_low(df, lookback):
    return df["close"].iloc[-1] < df["low"].rolling(lookback).min().iloc[-2]
