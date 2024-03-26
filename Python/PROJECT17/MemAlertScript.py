import psutil
import requests

TOKEN = ""
CHAT_ID = ""
# Threshold for memory usage (%)
THRESHOLD = 50

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

def check_memory_usage():
    memory_percent = psutil.virtual_memory().percent
    if memory_percent >= THRESHOLD:
        message = f"⚠️ Memory Usage Alert ⚠️\n\nCurrent Memory Usage: {memory_percent}%"
        send_telegram_message(message)

if __name__ == "__main__":
    check_memory_usage()