# telegram.py
import requests
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

def send_signal(market, symbol, tf, side, price):
    msg = (
        f"📡 LONG TERM SIGNAL\n"
        f"Market: {market}\n"
        f"Symbol: {symbol}\n"
        f"TF: {tf}\n"
        f"Side: {side}\n"
        f"Price: {price}"
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg}

    r = requests.post(url, json=payload)

    print("📨 Telegram response:", r.text)
