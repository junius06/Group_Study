import os
import urllib.request
import openai
import requests
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env', 'dev.env'))
API_KEY = os.getenv("OPENAI_API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# gpt가 제작하는 사진을 저장할 'outputs' 디렉터리가 없을 경우 생성
outputs = os.path.join(os.path.dirname(__file__), 'outputs')
if not os.path.exists(outputs):
    os.makedirs(outputs, exist_ok=True)

# Initialize the OpenAI client with the API key
openai.api_key = API_KEY

# Function to get user input with validation
def get_input(prompt, valid_options=None, value_map=None):
    while True:
        value_input = input(prompt)
        if valid_options:
            if value_input in valid_options:
                if value_map:
                    return value_map[value_input]
                return value_input
            else:
                print(f"Invalid input. Please choose from {valid_options}.")
        else:
            return value_input

# Define value maps for user inputs
model_map = {
    "1": "dall-e-2",
    "2": "dall-e-3"
}

d2_size_map = {
    "1": "256x256",
    "2": "512x512",
    "3": "1024x1024"
}

d3_size_map = {
    "1": "1024x1024",
    "2": "1024x1792",
    "3": "1792x1024"
}

quality_map = {
    "1": "hd",
    "2": "standard"
}

# Function to send a photo via Telegram
def send_photo(chat_id, image_path):
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

# Get inputs
image_name = get_input("1. Enter the name of image: ")
model = get_input("2. Enter the model (1. dall-e-2 / 2. dall-e-3): ", 
                  valid_options=["1", "2"],
                  value_map=model_map
                  )

if model=="dall-e-2":
    size_map = d2_size_map
    size_prompt = "(1. 256x256 / 2. 512x512 / 3. 1024x1024): "
elif model=="dall-e-3":
    size_map = d3_size_map
    size_prompt = "(1. 1024x1024 / 2. 1024x1792 / 3. 1792x1024): "
    
prompt = get_input("3. Enter image description: ")
size = get_input(f"4. Enter image size {size_prompt}", 
                 valid_options=["1", "2", "3"],
                 value_map=size_map
                 )

quality = get_input("5. Enter image quality (1. HD / 2. standard): ", 
                    valid_options=["1", "2"],
                    value_map=quality_map
                    )

# Generate images using OpenAI API
response = openai.Image.create(
    model=model,
    prompt=prompt,
    size=size,
    quality=quality,
    n=1
)

# Save the generated images and send them via Telegram
for i, data in enumerate(response['data']):
    import sys
    image_url = data['url']
    filename = os.path.join(outputs, f"{image_name}.jpg") # 생성된 이미지를 outputs 디렉터리에 저장
    urllib.request.urlretrieve(image_url, filename) # 이미지 다운로드
    print(f"Image saved {filename}")

    # Send the image via Telegram
    result = send_photo(CHAT_ID, filename)
    if result['ok']:
        print(result)
    else:
        print(f"Error {result['error_code']}: {result['description']}")
        sys.exit(1)

print("Image generation and sending completed.")