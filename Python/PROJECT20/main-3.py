# 책 예제 코드가 마음에 안들어서 내 편의대로 수정한 '실시간 검색 확인 코드'
# 뉴스 실시간 검색하기 위해 사용된 포털은 news.nate.com 뉴스이다. 
# news.google.com 등 다른 포털사이트에서의 검색어를 찾아오기 위해서는 해당 포털사이트에서 사용하는 객체 이름을 확인하여 수정해야 한다.

import requests
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup
import re

load_dotenv()
URL = os.getenv('nate_news_url', 'google.com') # url 변수가 지정되어 있지 않는 경우, url 변수는 google.com로 지정된다.
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
}

response = requests.get(URL)
soup = BeautifulSoup(response.text, 'html.parser')

# print(soup)

news_items = soup.select('a.lt1')

for idx, item in enumerate(news_items):
    if idx >= 10:  # 상위 10개 제목만 출력한다.
        break
    # <h2 class="tit"> 내부의 텍스트(제목)를 추출한다.
    title = item.find('h2', class_='tit').text.strip()
    title = re.sub(r"\[.*?\]", "", title)
    # href 속성(링크)을 추출한다.
    link = item.get('href')
    # 링크가 완전한 URL이 아니므로 접두사 'https' 추가한다.
    full_link = f"https:{link}" if link.startswith("//") else link
    print(f'{idx + 1}. Title: {title}\nLink: {full_link}\n')