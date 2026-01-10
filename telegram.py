# telegram.py
import requests
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_signal(symbol, tf, side, entry, tp, sl, confidence):
    msg = (
        f"📡 SMART TRADE SIGNAL\n"
        f"Symbol: {symbol}\n"
        f"TF: {tf}\n"
        f"Side: {side}\n"
        f"Entry: {entry}\n"
        f"🎯 TP (ATR): {tp}\n"
        f"🛑 SL (ATR): {sl}\n"
        f"📊 Confidence: {confidence}/100"
    )

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    r = requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": msg
    }, timeout=10)

    print("📨 Telegram:", r.text)
