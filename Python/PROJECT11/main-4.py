# 일정 간격마다 전송

import pyautogui
import pyperclip
import time
import threading
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def send_message():
    threading.Timer(10, send_message).start()
    
    picPosition = pyautogui.locateOnScreen('pic1.png')
    print(picPosition)
    
    if picPosition is None:
        picPosition = pyautogui.locateOnScreen('pic2.png')
        print(picPosition)
        
    if picPosition is None:
        picPosition = pyautogui.locateOnScreen('pic3.png')

    clickPosion = pyautogui.center(picPosition)
    pyautogui.doubleClick(clickPosion)
    
    pyperclip.copy("This is auto message.")
    pyautogui.hotkey("ctrl", "v")
    time.sleep(1.0)
    
    pyautogui.write(["enter"])
    time.sleep(1.0)
    
    pyautogui.write(["escape"])
    time.sleep(1.0)