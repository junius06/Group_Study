import os
import pandas as pd
import numpy as np
from numpy import dot
from numpy.linalg import norm
import ast
import openai
import streamlit as st
from streamlit_chat import message
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

folder_path = './data'
file_name = 'df_backup.csv'
file_path = os.path.join(folder_path, file_name)

if os.path.isfile(file_path):
    print(f'{file_name} 파일이 존재합니다.')
    df = pd.read_csv(file_path)
    df['embedding'] = df['embedding'].apply(ast.literal_eval)
    
else:
    txt_files = [file for file in os.listdir(folder_path) if file.endswith('.txt')]
    
    data = []
    
    for file in txt_files:
        file_path = os.path.join(folder_path, file)
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
            data.append(text)
            
    df = pd.DataFrame(data, columns=['text'])
    
    df['embedding'] = df.apply(lambda row: get_embedding(
        row.text,
    ), axis=1)
    
    df.to_csv(file_path, index=False, encoding='utf-8-sig')

def cos_sim(A, B):
    return dot(A, B) / (norm(A) * norm(B))

def return_answer_candidate(df, query):
    query_embedding = get_embedding(
        query,
    )
    
    df['similarity'] = df.embedding.apply(lambda x: cos_sim(np.array(x), np.array(query_embedding)))
    top_three_doc = df.sort_values('similarity', ascending=False).head(3)
    return top_three_doc

def create_prompt(df, query):
    result = return_answer_candidate(df, query)
    system_role = f"""You are an artificial intelligence language model named "정채기" that specializes in summarizing
    and answering documents about Seoul's youth policy, developed by developers 가나다 and 마바사.
    You need to take a given document and return a vert detailed summary of the document in the query language.
    Here are the document:
        doc 1 : """ + str(result.iloc[0]['text']) + """ 
        doc 2 : """ + str(result.iloc[1]['text']) + """
        doc 3 : """ + str(result.iloc[2]['text']) + """
    You must return in Korean. Return a accurate answer based on the document.
    """
    user_content = f"""User question: "{str(query)}". """
    
    messages = [
        {"role": "system", "content": system_role},
        {"role": "user", "content": user_content}
    ]
    return messages

def generate_response(messages):
    result = openai.ChatCompletion.create(
        model = "gpt-4o",
        messages = messages,
        temperature = 0.4,
        max_tokens = 500
    )
    return result.choices[0].message.content

try: 
    st.image('./images/ask_me_chatbot.png')
except Exception as e:
    print(e)

# 화면에 보여주기 위해 챗봇의 답변을 저장할 공간 할당
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
    
# 화면에 보여주기 위해 사용자의 답변을 저장할 공간 할당
if 'past' not in st.session_state:
    st.session_state['past'] = []
    
# 사용자의 입력이 들어오면 user_input에 저장하고 Send 버튼을 클릭하면 submitted의 값이 True로 변환
with st.form('form', clear_on_submit=True):
    user_input = st.text_input('정책을 물어보세요.', '', key='input')
    submitted = st.form_submit_button('Send')
    
# submitted의 값이 True면 챗본이 답변을 하기 시작
if submitted and user_input:
    prompt = create_prompt(df, user_input)
    chatbot_response = generate_response(prompt)
    # 화면에 보여주기 위해 사용자의 질문과 챗봇의 답변을 각각 저장
    st.session_state['past'].append(user_input)
    st.session_state['generated'].append(chatbot_response)
    
# 사용자의 질문과 챗봇의 답변을 순차적으로 화면에 출력
if st.session_state['generated']:
    for i in reversed(range(len(st.session_state['generated']))):
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        message(st.session_state['generated'][i], key=str(i))
