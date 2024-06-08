import tkinter
import tkinter.font
import pyupbit
import threading
import time
import logging

# 로깅 설정
logging.basicConfig(filename='app_health.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def check_health():
    try:
        logging.info("Health status: OK.")
    except Exception as e:
        logging.exception("Health status failed: %s", e)
    finally:
        window.after(600000, check_health) # 600000ms = 10m

coin_price = 0
def get_coin_price():
    global coin_price
    try:
        while True:
            coin_price = pyupbit.get_current_price("KRW-META")
            time.sleep(1.0)
    except Exception as e: # upbit API 호출 중 예외(에러 등) 발생시 로그 파일에 기록
        logging.exception("Error getting the coin price: %s", e)
        raise
        
t1 = threading.Thread(target=get_coin_price)
t1.daemon = True
t1.start()

window = tkinter.Tk()
window.title("METADIUM")
window.geometry("200x50")
window.resizable(False,False)

font = tkinter.font.Font(size = 30)
label = tkinter.Label(window, text="", font=font)
label.pack()

def get_coin_1sec():
    global coin_price
    try:
        now_btc_price = str(coin_price)
        label.config(text=now_btc_price)
        window.after(1000, get_coin_1sec)
    except Exception as e: # label 업데이트 중 예외 발생시 로그 파일에 기록
        logging.exception("Error updating the label: %s", e)
        raise
    
check_health()

get_coin_1sec()

window.mainloop()