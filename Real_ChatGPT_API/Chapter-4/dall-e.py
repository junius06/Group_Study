import os
import urllib.request
import openai
import urllib
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env', 'dev.env')) # os.path.dirname(__file__)는 현재 파일(API_1.py)을 가리킨다.
API_KEY = os.getenv("OPENAI_API_KEY")

# gpt가 제작하는 사진을 저장할 'outputs' 디렉터리가 없을 경우 생성
outputs = os.path.join(os.path.dirname(__file__), 'outputs')
if not os.path.exists(outputs): 
    os.makedirs(outputs, exist_ok = True)

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

# Function to log creating image messages


# Get inputs
image_name = get_input("1. Enter the name of image: ")
prompt = get_input("3. Enter image description: ")
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
    
size = get_input(f"4. Enter image size {size_prompt}", 
                 valid_options=["1", "2", "3"],
                 value_map=size_map
                 )

quality = get_input("5. Enter image quality (1. HD / 2. standard): ", 
                    valid_options=["1", "2"],
                    value_map=quality_map
                    )
# n = int(get_input("6. Enter number of images: "))

# Generate images using OpenAI API
response = openai.Image.create(
    model=model,
    prompt=prompt,
    size=size,
    quality=quality,
    n=1
)

# Save the generated images
for i, data in enumerate(response['data']):
    image_url = data['url']
    filename = os.path.join(outputs, f"{image_name}.jpg") # 생성된 이미지를 outputs 디렉터리에 저장
    urllib.request.urlretrieve(image_url, filename) # f"image_{i + 1}.jpg")
    print(f"Image saved {filename}")
    # print(f"Image {i + 1} saved as image_{i + 1}.jpg")

print("Image generation completed.")