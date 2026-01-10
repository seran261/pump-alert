# telegram.py
import requests
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_signal(market, symbol, tf, side, entry, tp, sl):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ Telegram env vars missing")
        return

    msg = (
        f"📡 LONG TERM SIGNAL\n"
        f"Market: {market}\n"
        f"Symbol: {symbol}\n"
        f"TF: {tf}\n"
        f"Side: {side}\n"
        f"Entry: {entry}\n"
        f"🎯 Take Profit: {tp}\n"
        f"🛑 Stop Loss: {sl}"
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    r = requests.post(url, json={
        "chat_id": TELEGRAM_CHAT_ID,
        "text": msg
    }, timeout=10)

    print("📨 Telegram response:", r.text)
