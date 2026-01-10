import pandas as pd

def moving_average(series, period):
    return series.rolling(period).mean()

def true_range(df):
    hl = df["high"] - df["low"]
    hc = (df["high"] - df["close"].shift()).abs()
    lc = (df["low"] - df["close"].shift()).abs()
    return pd.concat([hl, hc, lc], axis=1).max(axis=1)

def atr(df, period):
    return true_range(df).rolling(period).mean()

def volume_spike(volume, lookback, multiplier):
    avg = volume.rolling(lookback).mean()
    return volume.iloc[-1] > avg.iloc[-1] * multiplier

def breakout_high(df, lookback):
    return df["close"].iloc[-1] > df["high"].rolling(lookback).max().iloc[-2]

def breakout_low(df, lookback):
    return df["close"].iloc[-1] < df["low"].rolling(lookback).min().iloc[-2]
