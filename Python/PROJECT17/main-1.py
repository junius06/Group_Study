import telegram
import asyncio

TOKEN = "6944996198:AAEC1mKal88N4awS0TIMj0mdH8QyqA1zeDI"
BOT = telegram.Bot(token=TOKEN)

async def main():
    updates = await BOT.get_updates()
    for u in updates:
        print(u.message)
        
if __name__ == '__main__':
    asyncio.run(main())

# updates = BOT.getUpdates()
# for u in updates:
#     print(u.message)
    
# https://api.telegram.org/bot{TOKEN}/getUpdates



## Issues
# TypeError: 'coroutine' object is not iterable
# sys:1: RuntimeWarning: coroutine 'Bot.get_updates' was never awaited
# coroutine은 비동기식IO를 수행하는 객체이며 비동기 환경에서 기다려야 한다.
# 따라서 async 및 await를 사용해야 한다.