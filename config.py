# =========================
# GLOBAL SETTINGS
# =========================

TIMEFRAMES = ["1d"]
SCAN_INTERVAL = 60
SYMBOL_LIMIT = 200

# =========================
# TREND SETTINGS
# =========================

MA_PERIOD = 50

# =========================
# VOLUME SETTINGS
# =========================

VOLUME_LOOKBACK = 20
VOLUME_MULTIPLIER = 1.5

# =========================
# BREAKOUT SETTINGS
# =========================

BREAKOUT_LOOKBACK = 20

# =========================
# ATR SETTINGS
# =========================

ATR_PERIOD = 14
ATR_SL_MULTIPLIER = 1.5
ATR_TP_MULTIPLIER = 3.0

# =========================
# CONFIDENCE SCORE
# =========================

WEIGHT_TREND = 40
WEIGHT_VOLUME = 25
WEIGHT_BREAKOUT = 25
WEIGHT_ATR = 10

MIN_CONFIDENCE_SCORE = 60
