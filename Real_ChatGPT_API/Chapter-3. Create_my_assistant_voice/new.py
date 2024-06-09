import streamlit as st
# audiorecorder 패키지 추가
from audiorecorder import audiorecorder
import openai
import os
from datetime import datetime
from gtts import gTTS
from dotenv import load_dotenv
import base64

load_dotenv()

# Load environment variables from .env file
# apikey = os.getenv("apikey")

def STT(audio, apikey):
    filename='input.mp3'
    audio.export(filename, format="mp3")

    # 음원 파일 열기
    audio_file = open(filename, "rb")
    # whisper 모델을 활용해 텍스트 얻기
    client = openai.OpenAI(api_key = apikey)
    response = client.audio.transcriptions.create(model = "whisper-1", file = audio_file )
    audio_file.close()
    # 파일 삭제
    os.remove(filename)
    return response.text

# 3.9 질답 구하기
def ask_gpt(prompt, model, apikey):
    client = openai.OpenAI(api_key = apikey)
    response = client.chat.completions.create(model=model, messages=prompt)
    gptResponse = response.choices[0].message.content
    return gptResponse

def TTS(response):
    # gTTS를 활용하여 음성 파일 생성
    filename = 'output.mp3'
    tts = gTTS(text=response, lang="ko")
    tts.save(filename)

    # 음원 파일 자동 생성
    with open(filename, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio autoplay="True">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """

        st.markdown(md, unsafe_allow_html=True,)

    os.remove(filename)


def main():
    st.set_page_config(
        page_title="음성 비서 프로그램",
        layout="wide")

    st.header("음성 비서 프로그램")

    st.markdown("---")

    with st.expander("음성비서 프로그램에 관하여", expanded=True):
        st.write(
        """
        - 음성 비서 프로그램의 UI는 스트림릿을 활용했습니다.
        - STT(Speech-To-Text)는 OpenAI의 Whisper AI를 활용했습니다.
        - 답변은 OpenAI의 GPT 모델을 활용했습니다.
        - TTS(Text-to-Speech-To)는 구글의 Google Translate TTS를 활용했습니다.
        """
        )

        st.markdown("---")

    if "chat" not in st.session_state:
        st.session_state["chat"] = []

    # if "OPENAI_API" not in st.session_state:
    #     st.session_state["OPENAI_API"] = apikey

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "system",
                                         "content": "You are a thoughtful assistant. Respond to all input in 25 words and answer in korea"}]

    if "check_audio" not in st.session_state:
        st.session_state["check_reset"] = False

    with st.sidebar:

        api_key = st.text_input(label="OPENAI API 키", placeholder="Enter Your API Key", value="", type="password")

        # st.session_state["OPENAI_API"] = st.text_input(
        #     label= "OpenAI API Key", placeholder= "Enter your OpenAI API", value="", type="password")

        st.markdown("---")

        model = st.radio(label="GPT 모델", options=["gpt-4", "gpt-3.5-turbo"])

        st.markdown("---")

        if st.button(label="초기화"):
            st.experimental_rerun()

            st.session_state["chat"] = []
            st.session_state["messages"] = [{"role": "system", "content" : "You are a thoughtful assistant. Respond to all input in 25 words and answer in korea"}]
            st.session_state["check_reset"] = True

    col1, col2 = st.columns(2)
    with col1:
        # 왼쪽 영역 작성
        st.subheader("질문하기")
        # 음성 녹음 아이콘 추가
        audio = audiorecorder("클릭하여 녹음하기", "녹음 중...")
        if (audio.duration_seconds > 0) and (st.session_state["check_reset"]) == False:
            # 음성 재생
            st.audio(audio.export().read())
            # 음원 파일에서 텍스트 추출
            question = STT(audio, api_key)

            # 채팅을 시각화 하기 위해 질문 내용 저장
            now = datetime.now().strftime("%M:%S")
            st.session_state["chat"] = st.session_state["chat"]+[("User",now, question)]
            # GPT 모델을 넣을 프롬프트를 위해 질문 내용 저장
            st.session_state["message"] = st.session_state["messages"]+[{"role": "user", "content": question}]


    with col2:
        st.subheader("질문/답변")
        if (audio.duration_seconds > 0) and (st.session_state["check_reset"]==False):
            # chatGPT에게 답변 얻기
            response = ask_gpt(st.session_state["messages"], model, api_key)
            # GPT 모델에 넣을 프롬프트를 위해 답변 내용 저장
            st.session_state["message"] = st.session_state["messages"] + [{"role": "system", "content": response}]

            # 채팅 시각화를 위한 답변 내용 저장
            now = datetime.now().strftime("%M:%S")
            st.session_state["chat"] = st.session_state["chat"]+ [("bot", now, response)]
            # 채팅 형식으로 시각화 하기
            for sender, time, message in st.session_state["chat"]:
                if sender == "user":

                    st.write(f'< divstyle = "display:flex;align-items:center;"> <div style = "background-color:#007AFF;color:white;border-radius:12px;padding:8px 12px;margin- right:8px;" >{message}</div><div style = "font-size:0.8rem;color:gray;" > {time} </div> </div> ', unsafe_allow_html=True)
                else:
                    st.write(f'< divstyle = "display:flex;align-items:center;justify-content:flex-end;"> <div style = "background-color:lightgray;border-radius:12px;padding:8px12px;margin-left:8px;">{message}</div><div style="<div style = "font-size:0.8rem;color:gray;" > {time} </div> </div> ', unsafe_allow_html=True)
                    st.write("")
            TTS(response)
