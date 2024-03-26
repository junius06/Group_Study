# PROJECT-17. Telegram으로 스마트폰에 메세지 보내기
파이썬코드를 작성하여 텔레그램으로 메세지를 자동 발송하는 프로그램이다.

* * *

## Issues
### All. 비동기식
```bash
TypeError: 'coroutine' object is not iterable
sys:1: RuntimeWarning: coroutine 'Bot.get_updates' was never awaited
```
> coroutine은 비동기식IO를 수행하는 객체이며 비동기 환경에서 기다려야 한다.
> 따라서 async 및 await를 사용해야 한다.

### main-3. telegram Updater TypeError
```bash
updater = Updater(token=TOKEN, use_context=True)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: Updater.__init__() got an unexpected keyword argument 'token'
```
> python-telegram-bot 라이브러리 이슈로 추측
> [Issus Case]: https://github.com/python-telegram-bot/python-telegram-bot/issues/4049