import requests
import json

slack_webhook_url = ""

def sendSlackWebhook(strText):
    headers = {
        "Content-type": "application/json"
    }
    
    data = {
        "text" : strText
    }
    
    res = requests.post(slack_webhook_url, headers=headers, data=json.dumps(data))
    
    if res.status_code == 200:
        return "ok"
    else:
        return "error"
    
print(sendSlackWebhook("파이썬 코드 발송 테스트 메세지"))