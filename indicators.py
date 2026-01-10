# indicators.py
import pandas as pd

def moving_average(series, period):
    return series.rolling(period).mean()

def volume_spike(volume, period=20):
    avg_vol = volume.rolling(period).mean()
    return volume.iloc[-1] > avg_vol.iloc[-1]
