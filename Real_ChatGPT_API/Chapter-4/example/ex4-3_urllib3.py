import urllib3
import urllib.request

http = urllib3.PoolManager()

url = 'https://jsonplaceholder.typicode.com/posts/1'
data = {"title": "Created Post", "body": "Lorem ipsum", "userId": 5}

response = http.request('POST', url, fields=data)

print(response.data)

# urllib3 : 파이썬 환경에서 HTTP 통신을 할 수 있게 돕는 라이브러리
# 기본 내장 라이브러리이므로 별도의 설치없이 사용 가능
# 클라우드 서버에 배포할 때에도 설치하지 않아도 무관