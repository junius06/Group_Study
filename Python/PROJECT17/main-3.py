import telegram
from telegram.ext import Updater
from telegram.ext import MessageHandler, filters

TOKEN = "6944996198:AAEC1mKal88N4awS0TIMj0mdH8QyqA1zeDI"
CHAT_ID = "-4197382434"

BOT = telegram.Bot(TOKEN)

def send_message():
    BOT.send_message(chat_id=CHAT_ID, text="자동응답 모드입니다. '아침, 점심, 저녁' 중 하나를 입력하세요.")
    
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
updater.start_polling()

def handler(update, context):
    user_text = update.message.text
    if user_text == "아침":
        BOT.send_message(chat_id=CHAT_ID, text="먹었습니다.")
    elif user_text == "점심":
        BOT.send_message(chat_id=CHAT_ID, text="먹었어")
    elif user_text == "저녁":
        BOT.send_message(chat_id=CHAT_ID, text="아직")
    else:
        BOT.send_message(chat_id=CHAT_ID, text="다시 입력하세요.")

send_message()  # 자동응답 모드 메세지 발송

echo_handler = MessageHandler(filters.text, handler)
dispatcher.add_handler(echo_handler)

updater.start_polling()