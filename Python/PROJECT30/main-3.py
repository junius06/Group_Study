import tkinter
import tkinter.font

window = tkinter.Tk()
window.title("Stop Watch")
window.geometry("300x200")
window.resizable(False,False)

font = tkinter.font.Font(size = 30)
label = tkinter.Label(window, text="hello", font=font)
label.pack(expand=True)  # expand 옵션을 True로 설정
#label.pack()

cnt = 0
def get_coin_1sec():
    global cnt
    now_btc_price = str(cnt)
    cnt = cnt + 1
    label.config(text=now_btc_price)
    window.after(1000, get_coin_1sec)
    
get_coin_1sec()

window.mainloop()