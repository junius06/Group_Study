import numpy as np # 수치연산
import matplotlib.pyplot as plt # 그래프 그리기
from keras.models import Sequential # 신경망 모델을 생성하기 위한 모듈
from keras.layers import LSTM, Dense # 신경망 모델을 생성하기 위한 모듈
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

row = int(round(result_list.shape[0] * 0.9))
train = result_list[:row, :]

x_train = train[:, :-1]
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
y_train = train[:, -1]

x_test = result_list[row:, :-1]
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
y_test = result_list[row:, -1]

x_train.shape, x_test.shape

model = Sequential()
model.add(LSTM(windown_size, return_sequences=True, input_shape=(windown_size, 1)))
model.add(LSTM(64, return_sequences=False))
model.add(Dense(1, activation='linear'))
model.compile(loss='mse', optimizer='rmsprop')
model.summary()

model.fit(x_train, y_train,
          validation_data=(x_test, y_test),
          batch_size=10, # 데이터를 10개씩 묶어서 학습
          epochs=10) # 학습을 10회 진행

model.save(r'./samsumg.h5')

######### 실제값과 예측값에 대한 그래프 #########
pred = model.predict(x_test)

# 정규화된 예측값을 원래 값으로 변환
pred_price = [(i + 1) * window[0] for i in pred]

# 정규화된 테스트 값을 원래 값으로 변환
real_price = [(i + 1) * window[0] for i in y_test]
    
# 그래프 작성
fig = plt.figure(facecolor='white', figsize=(100, 15))
ax = fig.add_subplot(233) # 그리드 2행, 그리드 3열, subplot 위치 (2행 3열의 그리드에서 세 번째 위치)
ax.plot(real_price, label='Real Price')
ax.plot(pred_price, label='Predicted Price')
ax.legend()

# 그래프 레이아웃 조정
plt.tight_layout()
plt.show()