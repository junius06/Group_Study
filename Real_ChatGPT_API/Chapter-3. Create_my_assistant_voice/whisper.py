import os
import openai
from dotenv import load_dotenv

dotenv_path = '.env/dev.env'
load_dotenv(dotenv_path)

api_key = os.getenv('GPT_API_KEY')
openai.api_key = api_key
# client = openai.OpenAI(api_key = api_key)

# 녹음 파일 열기
audio_file = open("output.mp3", "rb")
# whisper 모델에 음원 파일 전달
transcript = openai.Audio.transcribe("whisper-1", audio_file)
# transcript = openai.transciption.create(model = "whisper-1", file = audio_file)

# 결과보기
print(transcript['text'])