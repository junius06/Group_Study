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

# 임베딩 함수 - 주어진 텍스트를 임베딩 벡터로 변환해주는 함수이다.
def get_embedding(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

# 임베딩을 계산할 텍스트 데이터를 리스트로 준비한다.
data = ['아침',
        '간식',
        '점심',
        '후식',
        '저녁',
        '야식'
        ]
# 준비한 데이터를 데이터프레임으로 변환한다. (행, 열)
df = pd.DataFrame(data, columns=['text'])
# print(f'임베딩 전 \n{df}')

# 임베딩 벡터를 계산하고 embedding열에 저장한다.
df['embedding'] = df.apply(lambda row: get_embedding(row.text), axis=1)
# print(f'임베딩 후 \n{df}')

# 벡터간의 유사도를 계산한다.
def cos_sim(A, B):
    return dot(A, B) / (norm(A) * norm(B))

# 쿼리 텍스트를 get_embedding() 함수로 임베딩하여 변환하고, query_embedding 변수에 저장한다.
def return_answer_candidate(df, query):
    query_embedding = get_embedding(
        query
    )
    # print(query_embedding) # query_embedding 변수에 저장된 내용 출력한다. (임베딩된 값이 출력되어 확인할 수 있음)
    
    # df에 존재하는 모든 embedding 열의 벡터들과 코사인 유사도를 계산하여 코사인 유사도가 가장 높은 상위 3개의 데이터를 찾아 반환한다.
        # embedding 열의 각 임베딩 데이터 'x'에 대해, query_embedding 과의 코사인 유사도를 계산한다. 그리고 이 값이 similarity 열에 저장된다.
    df["similarity"] = df.embedding.apply(lambda x: cos_sim(np.array(x), np.array(query_embedding)))
    # sort_values("similarity", ascending=False) -> similarity 열을 기준으로 데이터프레임을 유사도가 높은 순서대로 정렬한다. (내림차순)
    # head(3) -> 정렬된 데이터프레임에서 상위 3개의 행을 선택한다. 유사도가 가장 높은 3개의 텍스트가 선택된 것이다.
    top_three_doc = df.sort_values("similarity", ascending=False).head(3)
    return top_three_doc # [['text', 'similarity']] -> 이걸 연결하면 임베딩값은 빼고, 상위 3개의 텍스트값과 그에 대한 유사도만 출력도 가능하다.

# 47라인에 print한 값을 출력해볼 수 있다. data에 있는 값들이 임베딩되어 저장되어 있고, 그 증 df라는 데이터의 임베딩값을 출력한다.
# return_answer_candidate(df, "아침")

# return_answer_candidate() 함수를 사용해서 '오전' 라는 텍스트와 임베딩 벡터값이 가장 유사한 상위 3개의 데이터를 출력한다.
sim_result = return_answer_candidate(df, '오전')
print(sim_result)



'''
** 동작순서 **
1. 변수에 텍스트 데이터를 입력한다.
2. 쿼리 텍스트를 임베딩 벡터로 변환한다.
3. 각 테스트 임베딩 벡터와 쿼리 임베딩 벡터 간의 유사도를 계산해서 similarity 열에 저장한다.
4. 유사도가 높은 순서대로 데이터프레임을 정렬하고 상위 3개의 텍스트를 선택한다.
5. 유사한 상위 3개의 텍스트와 그 유사도 값을 포함하는 데이터프레임을 반환한다.
'''