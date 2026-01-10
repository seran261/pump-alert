import requests
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_signal(symbol, tf, side, entry, sl, tp1, tp2, tp3, confidence):
    msg = (
        f"📡 SMART TRADE SIGNAL\n"
        f"Symbol: {symbol}\n"
        f"TF: {tf}\n"
        f"Side: {side}\n"
        f"Entry: {entry}\n"
        f"🛑 SL: {sl}\n"
        f"🎯 TP1: {tp1}\n"
        f"🎯 TP2: {tp2}\n"
        f"🎯 TP3: {tp3}\n"
        f"📊 Confidence: {confidence}/100"
    )

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    r = requests.post(
        url,
        json={"chat_id": CHAT_ID, "text": msg},
        timeout=10
    )

    print("📨 Telegram:", r.text)
