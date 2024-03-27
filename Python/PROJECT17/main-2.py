import telegram
import asyncio

TOKEN = "6944996198:AAEC1mKal88N4awS0TIMj0mdH8QyqA1zeDI"
CHAT_ID = "-4158176851"

# bot = telegram.Bot(TOKEN)
# bot.sendMessage(chat_id=CHAT_ID, text="테스트 메세지")

async def send_async_message():
    BOT = telegram.Bot(TOKEN)
    await BOT.send_message(chat_id=CHAT_ID, text="테스트 메세지")

if __name__ == '__main__':
    asyncio.run(send_async_message())