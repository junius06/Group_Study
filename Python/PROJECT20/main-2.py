from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
URL = 'https://signal.bz/news'

driver.get(url=URL)
driver.implicitly_wait(time_to_wait=5)

naver_results = driver.find_elements(By.CSS_SELECTOR, '#app > div > main > section > div > section > section:nth-child(2) > div:nth-child(2) > div > div > div > a > span.rank-text')

naver_list = []
for naver_result in naver_results:
    print(naver_result.text)
    naver_list.append(naver_result.text)

driver.quit()