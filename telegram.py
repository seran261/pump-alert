import requests
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_signal(symbol, tf, side, entry, sl, tp1, tp2, tp3, confidence):
    direction_emoji = "🟢🚀" if side == "BUY" else "🔴📉"
    confidence_emoji = (
        "🔥🔥" if confidence >= 85 else
        "🔥" if confidence >= 70 else
        "✨"
    )

    msg = (
        f"{direction_emoji}  *SMART TRADE SIGNAL*  {direction_emoji}\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"

        f"🪙 *Symbol* : `{symbol}`\n"
        f"⏱ *TF*      : `{tf}`\n"
        f"📊 *Trend*  : *{side}*\n\n"

        f"💰 *ENTRY ZONE*\n"
        f"➤ Entry : `{entry}`\n\n"

        f"🛑 *RISK CONTROL*\n"
        f"➤ Stop Loss : `{sl}` ❌\n\n"

        f"🎯 *TAKE PROFIT LADDER*\n"
        f"➤ TP1 : `{tp1}` 🎯\n"
        f"➤ TP2 : `{tp2}` 🎯🎯\n"
        f"➤ TP3 : `{tp3}` 🎯🎯🎯\n\n"

        f"{confidence_emoji} *CONFIDENCE SCORE*\n"
        f"➤ `{confidence}/100`\n\n"

        f"⚡ *Strategy* : ATR • HTF Trend • Volume/Breakout\n"
        f"⏳ *Status*   : Waiting for execution\n\n"

        f"━━━━━━━━━━━━━━━━━━\n"
        f"🤖 *Auto Signal Bot*"
    )

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    r = requests.post(
        url,
        json={
            "chat_id": CHAT_ID,
            "text": msg,
            "parse_mode": "Markdown"
        },
        timeout=10
    )

    print("📨 Telegram:", r.text)
