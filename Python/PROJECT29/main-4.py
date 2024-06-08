import streamlit as st
import datetime
import pyupbit
import time

# 10초마다 캐시를 갱신
@st.cache_data(ttl=10)
def get_data(ticker, interval, to, count):
    return pyupbit.get_ohlcv(ticker=ticker, interval=interval, to=to, count=count)

def main():
    st.title("암호화폐 시세 분석")
    
    # 코인 선택
    ticker = st.selectbox(
        '암호화폐를 선택하세요',
        options=['KRW-BTC', 'KRW-ETH', 'KRW-META']
    )

    # 날짜 선택
    d = st.date_input("날짜를 선택하세요.", datetime.date.today())
    st.write(f'{ticker} 1일 차트')

    # 시간 간격 선택
    interval = st.selectbox(
        '시간 간격을 선택하세요',
        options=['minute1', 'minute3', 'minute5', 'minute10', 'minute15', 'minute30', 'minute60', 'day', 'week']
    )
    
    # 차트 컨테이너
    chart_placeholder = st.empty()
    
    # 주기적 업데이트
    while True:
        to = str(d + datetime.timedelta(days=1))
        count = 24
        price_now = get_data(ticker, interval, to, count)

        with chart_placeholder.container():
            st.line_chart(price_now[['open', 'high', 'low', 'close']])
            st.write("선택된 날짜에 대한 가격 통계")
            st.write(price_now.describe())

        time.sleep(10)  # 10초마다 데이터 갱신

# 메인 함수 실행
if __name__ == '__main__':
    main()