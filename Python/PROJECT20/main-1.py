# from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver

driver = webdriver.Chrome()

URL = 'https://www.google.com'

driver.get(url=URL)
driver.implicitly_wait(time_to_wait=10) # time_to_wait 초 단위 시간 값을 입력한다.