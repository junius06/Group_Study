# 텔레그램 봇을 이용하여 메세지 전송

import urllib3
import json

BOT_TOKEN = ""
CHAT_ID = ""

def sendMessage(chat_id, text):
    data = {
        'chat_id': chat_id,
        'text': text,
    }
    http = urllib3.PoolManager()
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    response = http.request('POST', url, fields=data)
    return json.loads(response.data.decode('utf-8'))

updates = sendMessage(CHAT_ID, "Hello. I am Telegram Bot.")
print(updates)