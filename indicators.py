# indicators.py
import pandas as pd

def moving_average(series, period):
    return series.rolling(period).mean()

def volume_spike(volume, lookback, multiplier):
    avg = volume.rolling(lookback).mean()
    return volume.iloc[-1] > avg.iloc[-1] * multiplier
