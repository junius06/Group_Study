import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import LSTM, Dense
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override()

now = datetime.now()
before = now - relativedelta(years=10)

now_day = now.strftime("%Y-%m-%d")
before_day = before.strftime("%Y-%m-%d")

print(f"start : {before_day}")
print(f"now : {now_day}")

samsung_stock = pdr.get_data_yahoo("005930.KS", start=before_day, end=now_day) # 005930 = 삼성전자 주식코드 / KS = 한국 주식 시세
print(samsung_stock)

close_prices = samsung_stock['Close'].values
print(close_prices)

windown_size = 30

result_list = []
for i in range(len(close_prices) - (windown_size + 1)):
    result_list.append(close_prices[i: i + (windown_size + 1)])

normal_data = []
for window in result_list:
    window_list = [((float(p) / float(window[0])) - 1) for p in window]
    normal_data.append(window_list)
    
result_list = np.array(normal_data)
print(result_list.shape[0], result_list.shape[1])