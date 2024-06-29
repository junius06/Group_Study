import os
import time
import openai
import threading
import queue as q
from dotenv import load_dotenv
from fastapi import Request, FastAPI

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env', 'dev.env'))
API_KEY = os.getenv("OPENAI_API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

openai.api_key = API_KEY

def txtResFormat(bot_res):
    res = {"version": "2.0", "template": { 
        "outputs": [
            {
                "simpleText": {
                    "text": bot_res
                }
            }
        ], 
        "quickReplies": []
    }}
    return res

def imgResFormat(bot_res, prompt):
    output_txt = prompt + "내용에 관한 이미지입니다."
    res = {"version": "2.0", "template": {
        "outputs": [
            {
                "simpleImg": {
                    "imgURL": bot_res, "altTxt": output_txt
                }
            }
        ], 
        "quickReplies": []
    }}
    return res

def timeover():
    res = {"version": "2.0", "template": {
        "outputs": [
            {
                "simpleTxt": {
                    "txt": "Creating Image.....\n잠시 후 아래 말풍선 클릭"
                }
            }
        ],
        "quickReplies": [
            {
                "action": "message",
                "label": "done",
                "msgTxt": "You done?"
            }
        ]
    }}
    return res

def getTxtFromGPT(prompt):
    msg_prompt = [{"role": "system", "content": "You are a 어쩌고"}]
    msg_prompt += [{"role": "system", "content": prompt}]
    res = openai.chat.completions.create(model="gpt-4o", msg=msg_prompt)
    
def getImgURLFromDallE(messages):
    res = openai.images.generate(
        model="dall-e-3",
        prompt=messages,
        size="1024x1024",
        quality="standard",
        n=1
    )
    img_url = res.data[0].url
    return img_url

def dbReset(filename):
    with open(filename, 'w') as f:
        f.write("")