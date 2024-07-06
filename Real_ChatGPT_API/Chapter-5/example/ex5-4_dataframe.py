import os
import openai
import numpy as np
import pandas as pd
from numpy import dot
from numpy.linalg import norm
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env', 'dev.env'))
API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = API_KEY

def get_embedding(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

# print(get_embedding('임베딩테스트'))

data = ['아침',
        '간식',
        '점심',
        '후식',
        '저녁',
        '야식'
        ]

df = pd.DataFrame(data, columns=['text']) # text는 변수 data에 저장된 데이터들의 열 이름이 된다. 여기의 열 이름이 바뀌면 35라인의 row.text 에서도 열 명칭이 동일하게 바뀌어야 한다.
print(f'임베딩 전 \n{df}')

# df['embedding'] 에서  embedding은 데이터가 저장될 열의 이름이 된다.
df['embedding'] = df.apply(lambda row: get_embedding(row.text), axis=1) # 위 data.colums text열에 저장된 값을 가져온다.
print(f'\n임베딩하여 벡터로 변환 : \n{df}')