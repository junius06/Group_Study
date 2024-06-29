# 기본 정보 설정

import os
import urllib3
import json
import openai
from dotenv import load_dotenv
from fastapi import Request, FastAPI

# Load environment variables from the .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env', 'dev.env'))
API_KEY = os.getenv("OPENAI_API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

openai.api_key = API_KEY


#######################################
########### Define function ###########
#######################################

# 메세지 전송
def sendMessage(chat_id, text, msg_id):
    data = {
        'chat_id': chat_id,
        'text': text,
        'reply_to_message_id': msg_id
    }
    http = urllib3.PoolManager()
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    response = http.request('POST', url, fields=data)
    return json.loads(response.data.decode('utf-8'))

# 사진 전송
def sendPhoto(chat_id, photo, msg_id):
    data = {
        'chat_id': chat_id,
        'photo': photo,
        'reply_to_msg_id': msg_id
    }
    http = urllib3.PoolManager()
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    response = http.request('POST', url, fields=data)
    return json.loads(response.data.decode('utf-8'))

# ChapGPT 질문/응답
def getTextFromGPT(messages):
    messages_prompt = [{"role": "system"}, {"content": 'You are a thoughtful assistant. Respond to all input in 25 words and answer in korea.'}]
    messages_prompt += [{"role": "system"}, {"content": messages}]
    response = openai.chat.completions.create(model="gpt-4o", messages=messages_prompt)
    system_message = response.choices[0].message.content
    return system_message

# Dall-e 에게 요청하여 그림 url 받기
def getImageURLFromDALLE(messages):
    response = openai.images.generate(
        model="dall-e-3",
        prompt=messages,
        size="1024x1024",
        quality="standard",
        n=1
    )
    image_url = response.data[0].url
    return image_url