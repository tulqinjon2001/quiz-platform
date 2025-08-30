import httpx
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_result(name: str, phone: str, score: int):
    message = f"📋 Test natijasi:\n👤 Ism: {name}\n📱 Tel: {phone}\n✅ Ball: {score}/30"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        httpx.post(url, json=payload)
    except Exception as e:
        print("Xatolik Telegramga yuborishda:", e)
