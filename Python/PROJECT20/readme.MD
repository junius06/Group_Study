# PROJECT-20. 실시간 검색어 모아보기
실시간 검색어를 추출하기 위한 프로그램을 작성한다.
해당 프로젝트의 코드를 작성하면서 라이브러리 버전 이슈가 발생하기 때문에, 최신 라이브러리를 찾고 비교하며 코드를 수정해야 한다.

* * *

## Issues
### 라이브러리 버전
```bash
Traceback (most recent call last):
  File "/usr/local/lib/python3.12/site-packages/selenium/webdriver/common/driver_finder.py", line 38, in get_path
    path = SeleniumManager().driver_location(options) if path is None else path
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/selenium/webdriver/common/selenium_manager.py", line 87, in driver_location
    browser = options.capabilities["browserName"]
              ^^^^^^^^^^^^^^^^^^^^
AttributeError: 'str' object has no attribute 'capabilities'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/jhkim/learning/Github/Group_Study/Python/PROJECT21/main-1.py", line 4, in <module>
    driver = webdriver.Chrome(ChromeDriverManager().install())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/selenium/webdriver/chrome/webdriver.py", line 45, in __init__
    super().__init__(
  File "/usr/local/lib/python3.12/site-packages/selenium/webdriver/chromium/webdriver.py", line 49, in __init__
    self.service.path = DriverFinder.get_path(self.service, options)
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/selenium/webdriver/common/driver_finder.py", line 40, in get_path
    msg = f"Unable to obtain driver for {options.capabilities['browserName']} using Selenium Manager."
                                         ^^^^^^^^^^^^^^^^^^^^
AttributeError: 'str' object has no attribute 'capabilities'
```
> from webdriver_manager.chrome import ChromeDriverManager
> chromeDriver = webdriver.Chrome(ChromeDriverManager().install())
> 위와 같이 webdriver_manager 라이브러리를 가져와서 ChromeDriverManager().install()를 호출하려면 에러가 발생한다.
> chromeDriver = webdriver.Chrome() 로 변경하면 이슈가 해결된다.
> 3.x 버전과 4.x 버전의 차이점에 대한 이슈이다.