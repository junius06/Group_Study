import pyupbit
import json

# KRW 마켓의 모든 코인 목록 가져오기
coin_lists = pyupbit.get_tickers(fiat='KRW')
# print(coin_lists)
print(json.dumps({"coin_lists": coin_lists}, indent=4))

# 비트코인과 이더리움의 한국 시세 출력
price_now = pyupbit.get_current_price(["KRW-BTC", "KRW-ETH"])
# print(price_now)
print(json.dumps({"price_now": price_now}, indent=4))