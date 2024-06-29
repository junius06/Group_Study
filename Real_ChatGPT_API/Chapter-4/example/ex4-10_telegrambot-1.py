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