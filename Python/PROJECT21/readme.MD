# PROJECT-21. 핫딜 알리미
책에서는 '뽐뿌'라는 사이트에서 제목을 출력하여 특정 단어가 포함되어 있을 경우 텔레그램으로 발송하는 코드를 작성한다.
그러나 핫딜 알림은 

* * *

## Issues
### 
```bash
RuntimeWarning: coroutine 'Bot.send_message' was never awaited
  bot.sendMessage(chat_id=chat_id, text=message)
RuntimeWarning: Enable tracemalloc to get the object allocation traceback
```
> bot.sendMessage 함수가 비동기 코루틴이기 때문에 발생하는 이슈이다.
> python-telegram-bot 라이브러리에서는 많은 함수들이 비동기로 동작한다.
> 따라서 비동기 함수를 호출할 때는 'await'를 사용하며, 이를 위해 비동기 환경이 필요하다.
> asyncio 라이브러리를 사용하여 비동기적으로 메시지를 보내는 함수를 정의할 수 있다.