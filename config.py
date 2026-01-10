# =========================
# TIMEFRAMES
# =========================

LOWER_TF = "4h"
HIGHER_TF = "1d"

SCAN_INTERVAL = 60

# =========================
# BTC DOMINANCE FILTER
# =========================

BTC_DOMINANCE_MAX = 52.0   # % → block alt BUY above this
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
# ATR
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

MIN_CONFIDENCE_SCORE = 60
