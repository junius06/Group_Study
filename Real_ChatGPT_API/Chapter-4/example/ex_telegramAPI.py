import os
import requests
from dotenv import load_dotenv

# Load dotenv file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env', 'dev.env'))
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Check if BOT_TOKEN is correctly loaded | BOT_TOKEN 값이 셋팅되어 있지 않을 때 반환 로그
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set. Please check your .env file.")

# Define function to send image & result log | 이미지 전송 & 결과 로그 함수 정의
def sendPhoto(chat_id, image_path):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    files = {'photo': open(image_path, 'rb')}
    data = {'chat_id': chat_id}
    response = requests.post(url, files=files, data=data)
    response_data = response.json()
    
    if response_data.get('ok'):
        return {'ok': True}
    else:
        error_code = response_data.get('error_code')
        description = response_data.get('description')
        return {'ok': False, 'error_code': error_code, 'description': description}

# Define function a latest image | 최신 이미지 함수 정의
def get_latest_image(directory):
    files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    if not files:
        return None
    latest_file = max(files, key=os.path.getctime)
    return latest_file

# 메인함수 실행
if __name__ == "__main__":
    import sys
    outputs_dir = os.path.join(os.path.dirname(__file__), 'outputs') # __file__ 현재 실행중인 python 파일 경로를 지정하고, os.path.dirname(__file__) 현재 실행되는 파이썬 파일이 있는 경로의 디렉터리만 추출 & 현재 디렉터리 경로에서 outputs 디렉터리로 이동
    latest_image = get_latest_image(outputs_dir) # get_latest_image 함수는 지정된 디렉터리에서 가장 최근에 생성된 파일을 찾아 반환하므로, 위 디렉터리(example/outputs) 내에서 최신 파일을 지정

    if not latest_image: # 최신 이미지 없으면 종료
        print(f"No images found in {outputs_dir}.")
        sys.exit(1)

    result = sendPhoto(CHAT_ID, latest_image) # 텔레그램 봇으로 최신 이미지 전송
    
    if result['ok']:
        print(result)
    else:
        print(f"Error {result['error_code']}: {result['description']}")
        sys.exit(1)