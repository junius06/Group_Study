# 기본 정보 설정
import os
import openai
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env', 'dev.env'))
API_KEY = os.getenv("OPENAI_API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


#######################################
########### Define function ###########
#######################################

# Send messages
def sendMessage(chat_id, text, msg_id):
    return

# Send Image
def sendPhoto(chat_id, image_url, msg_id):
    return

# Ask a question to ChatGPT & Get a answers from ChatGPT
def getTextFromGPT(messages):
    return

# Ask a photo to ChatGPT DALL.E & Get a image from ChatGPT DALL.E
def getImageURLFromDALLE(messages):
    return


#######################################
############ Create server ############
#######################################
# fastAPI 이용하여 코드 작성



#######################################
############ Main Function ############
#######################################
# 메인함수 실행