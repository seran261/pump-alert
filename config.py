# =========================
# MARKET MODE
# =========================
MARKET_TYPE = "FUTURES"   # BYBIT USDT Perpetuals

# =========================
# TIMEFRAMES (BYBIT)
# =========================
LOWER_TF = "240"   # 4H in minutes
HIGHER_TF = "D"    # 1D

SCAN_INTERVAL = 60

# =========================
# BTC DOMINANCE FILTER
# =========================
BTC_DOMINANCE_MAX = 52.0
ALLOW_BTC_ALWAYS = True

# =========================
# TREND
# =========================
MA_PERIOD = 50

# =========================
# VOLUME
# =========================
VOLUME_LOOKBACK = 20
VOLUME_MULTIPLIER = 1.5

# =========================
# BREAKOUT
# =========================
BREAKOUT_LOOKBACK = 20

# =========================
# ATR / RISK
# =========================
ATR_PERIOD = 14
ATR_SL_MULTIPLIER = 1.5

TP1_ATR = 1.0
TP2_ATR = 2.0
TP3_ATR = 3.0

# =========================
# CONFIDENCE
# =========================
WEIGHT_TREND_LTF = 25
WEIGHT_TREND_HTF = 30
WEIGHT_VOLUME = 15
WEIGHT_BREAKOUT = 20
WEIGHT_ATR = 10

MIN_CONFIDENCE_SCORE = 45   # relaxed for futures
