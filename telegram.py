import requests
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

API_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"


# =========================
# UTILS
# =========================

def confidence_bar(score, length=10):
    filled = int((score / 100) * length)
    empty = length - filled
    return "▓" * filled + "░" * empty


def market_sentiment(side):
    return "🐂 Bullish" if side == "BUY" else "🐻 Bearish"


def send(msg):
    r = requests.post(
        API_URL,
        json={
            "chat_id": CHAT_ID,
            "text": msg,
            "parse_mode": "Markdown"
        },
        timeout=10
    )
    print("📨 Telegram:", r.text)


# =========================
# MAIN SIGNAL MESSAGE
# =========================

def send_signal(symbol, tf, side, entry, sl, tp1, tp2, tp3, confidence):
    direction_emoji = "🟢🚀" if side == "BUY" else "🔴📉"
    fire = "🔥🔥" if confidence >= 85 else "🔥" if confidence >= 70 else "✨"

    msg = (
        f"{direction_emoji} *SMART TRADE SIGNAL* {direction_emoji}\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"

        f"🪙 *Symbol* : `{symbol}`\n"
        f"⏱ *TF*      : `{tf}`\n"
        f"🧠 *Bias*   : *{market_sentiment(side)}*\n\n"

        f"💰 *ENTRY*\n"
        f"➤ `{entry}`\n\n"

        f"🛑 *STOP LOSS*\n"
        f"➤ `{sl}` ❌\n\n"

        f"🎯 *TAKE PROFIT LADDER*\n"
        f"➤ TP1 : `{tp1}` 🎯\n"
        f"➤ TP2 : `{tp2}` 🎯🎯\n"
        f"➤ TP3 : `{tp3}` 🎯🎯🎯\n\n"

        f"{fire} *CONFIDENCE*\n"
        f"`{confidence}/100`\n"
        f"`{confidence_bar(confidence)}`\n\n"

        f"⚡ *Strategy* : ATR • HTF Trend • Volume/Breakout\n"
        f"⏳ *Status*   : Monitoring price...\n\n"

        f"━━━━━━━━━━━━━━━━━━\n"
        f"🤖 *Auto Signal Bot*"
    )

    send(msg)


# =========================
# TP HIT FOLLOW-UPS
# =========================

def send_tp_hit(symbol, tp_level, price):
    emojis = {
        1: "🎯✨",
        2: "🎯🎯🔥",
        3: "🎯🎯🎯🚀"
    }

    msg = (
        f"{emojis.get(tp_level, '🎯')} *TAKE PROFIT HIT*\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        f"🪙 `{symbol}`\n"
        f"🎯 TP{tp_level} reached\n"
        f"💰 Price : `{price}`\n\n"
        f"🔁 Consider securing profits\n"
        f"━━━━━━━━━━━━━━━━━━"
    )

    send(msg)


# =========================
# TRAILING SL UPDATE
# =========================

def send_trailing_sl(symbol, new_sl):
    msg = (
        f"🔁🛡 *TRAILING STOP UPDATED*\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        f"🪙 `{symbol}`\n"
        f"🛑 New SL : `{new_sl}`\n\n"
        f"🔒 Risk reduced • Trade protected\n"
        f"━━━━━━━━━━━━━━━━━━"
    )

    send(msg)


# =========================
# SIGNAL EXPIRY
# =========================

def send_signal_expired(symbol):
    msg = (
        f"⏰❌ *SIGNAL EXPIRED*\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        f"🪙 `{symbol}`\n"
        f"⌛ Entry window closed\n\n"
        f"📭 Signal no longer valid\n"
        f"━━━━━━━━━━━━━━━━━━"
    )

    send(msg)
