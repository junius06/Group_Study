# 사진에서 좌표 추출

import pyautogui
import os

# 라이브러리 버전이슈?
import pyscreeze
import PIL

pyscreeze.PIL__version__ = tuple(int(x) for x in PIL.__version__.split("."))

# change directory : .py파일을 실행하는 경로로 이동
os.chdir(os.path.dirname(os.path.abspath(__file__)))

picPosition = pyautogui.locateOnScreen('pic1.png')
print(picPosition)

if picPosition is None:
    picPosition = pyautogui.locateOnScreen('pic2.png')
    print(picPosition)

if picPosition is None:
    picPosition = pyautogui.locateOnScreen('pic3.png')
    print(picPosition)