import openai
import os
from dotenv import load_dotenv

dotenv_path = '.env/dev.env'
load_dotenv(dotenv_path)

api_key = os.getenv('GPT_API_KEY', 'xxxxxxxxxxxxxxxx')
openai.api_key = api_key
# client = openai.OpenAI(api_key = api_key)

audio_file = open("output.mp3", "rb")
transcript = openai.Audio.transcribe("whisper-1", audio_file)
# transcript = openai.transciption.create(model = "whisper-1", file = audio_file)

print(transcript['text'])