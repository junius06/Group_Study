# PROJECT-11. 오토마우스를 활용한 PC카카오톡 자동화
오토마우스를 활용하여 PC에 설치된 카카오톡을 통해 메세지를 자동으로 보내는 프로그램을 만든다.   
해당 기능은 카카오톡을 통해 메세지를 자동으로 보내는 것 외에도, 매크로와 같은 여러가지 프로그램을 구현할 수 있다.   

* * *

## Issues

> ### Issue-1. Python Interpreter
> - python3.12 로 진행했더니, 사진과 같이 라이브러리 "pyautogui, pyperclip"에서 문제가 발생했다.
> ![library warning](issue_pics/library.jpg)
> - python3.11 로 설정하였더니 해당 이슈는 해결되었다.
> ![library warning](/Python/PROJECT11/issue_pics/select_interpreter.jpg)
> - 라이브러리 pyautogui 설치시 python3.11 로 설치되었던 것을 확인할 수 있었다.
> ![library warning](issue_pics/install_pyautogui.jpg)

> ### Issue-2. [Screenshot] '<' not supported between instances of 'str' and 'int'
> - 스크린샷이 정상적으로 수행되지 않는 이슈가 발생했다.
> - 아래와 같이 코드 추가 후 스크린샷이 잘 동작되었다.
> ```bash
> import pyscreeze
> import PIL
> 
> pyscreeze.PIL__version__ = tuple(int(x) for x in PIL.__version__.split("."))
> ```
>- 에러내용
>```bash
>Traceback (most recent call last):
>  File "/Users/jhkim/learning/my-github/Group_Study/Python/20240313/PROJECT11/main-1.py", line 15, in <module>
>    picPosition = pyautogui.locateOnScreen('pic1.png')
>                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
>  File "/usr/local/lib/python3.11/site-packages/pyautogui/__init__.py", line 172, in wrapper
>    return wrappedFunction(*args, **kwargs)
>           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
>  File "/usr/local/lib/python3.11/site-packages/pyautogui/__init__.py", line 210, in locateOnScreen
>    return pyscreeze.locateOnScreen(*args, **kwargs)
>           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
>  File "/usr/local/lib/python3.11/site-packages/pyscreeze/__init__.py", line 375, in locateOnScreen
>    screenshotIm = screenshot(
>                   ^^^^^^^^^^^
>  File "/usr/local/lib/python3.11/site-packages/pyscreeze/__init__.py", line 527, in _screenshot_osx
>    if tuple(PIL__version__) < (6, 2, 1):
>       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
>TypeError: '<' not supported between instances of 'str' and 'int'
>```
>[Github_Ticket](https://github.com/asweigart/pyautogui/issues/790)

> ### Issue-3. [None] Image not found
> - 위의 두 에러를 조치한 후 코드가 실행되며 이미지를 찾도록 수행되었지만, pic1~3.png 이미지의 좌표를 찾지 못 하고 None을 반환했다.