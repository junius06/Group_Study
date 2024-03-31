import telegram
from dotenv import load_dotenv
import os
import subprocess
import asyncio

load_dotenv()

bot_token = os.getenv('bot_token', 'xxxxxxxxxxxxxxxx')
chat_id = os.getenv('chat_id', '-xxxxxxxx')
bot = telegram.Bot(bot_token)

# process = subprocess.Popen(['python3', '../PROJECT20/main-3.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# stdout, stderr = process.communicate()
# output = stdout.decode().split('\n')
# 
# for line in output:
#     if "Title" in line:
#         message = line.strip()
#         print(message)
#         bot.sendMessage(chat_id=chat_id, text=message)

# 비동기 함수로 sendMessage 호출
async def send_message(chat_id, text):
    loop = asyncio.get_event_loop()
    await bot.send_message(chat_id=chat_id, text=text)

# 메인 로직을 비동기 함수로 정의
async def main():
    process = subprocess.Popen(['python3', '../PROJECT20/main-3.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    output = stdout.decode().split('\n')
    
    for line in output:
        if "Title" in line:
            message = line.strip()
            print(message)
            await send_message(chat_id, message)

# 이벤트 루프를 생성하고 main() 코루틴을 실행
asyncio.run(main())