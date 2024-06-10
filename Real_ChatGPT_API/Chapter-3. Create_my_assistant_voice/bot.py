import os
import openai
import streamlit as st
from audiorecorder import audiorecorder
# 시간정보를 위한 패키지
from datetime import datetime

##### implementation function #####
def STT(audio, apikey):
  # 파일저장
  filename = 'input.mp3'
  audio.export(filename, format='mp3')
  
  # 음원 파일 열기
  audio_file = open(filename, 'rb')
  # whisper 모델을 활용해 텍스트 얻기
  client = openai.OpenAI(api_key = apikey)
  respons = client.audio.transscriptions.create(model = "whisper-1", file = audio_file)
  audio_file.close()
  # 파일 삭제
  os.remove(filename)
  return respons.text

def ask_gpt(prompt, model, apikey): # 질문 텍스트와 LLM모델을 입력으로 받고, ChatGPT의 답변을 반환하는 함수 askgpt() 선언
  client = openai.OpenAI(api_key = apikey)
  response = client.chat.completions.create(
    model=model, # st.session_state["model"] 라디오 버튼으로 선택한 모델로 설정
    messages=prompt # 입력받은 프롬프트를 활용하여 질문 
  )
  gptResponse = response.choices[0].message.content # GPT 모델을 통해 얻은 최종 답변 저장
  return gptResponse

##### main function #####
def main():
  # 기본 설정
  st.set_page_config(
    page_title="Voice Assistant",
    layout="wide"
    )

  st.header("Voice Assistant Program")

  st.markdown("---")
  
  ## 텍스트로 기본 설명
  with st.expander("about voice assistant", expanded=True):
    st.write(
    """
    - Used streamlit
    - Used Whisper AI of OpenAI for STT(Speach-to-Text)
    - Used OpenAI Model
    - Used Google translate TTS(Text-to-Speach)
    """
    )
    
    st.markdown("")

  ## session state 초기화
  if "chat" not in st.session_state:
    st.session_state["chat"] = [] # 사용자와 음성 비서의 대화 내용을 저장하여 채팅창에 표시

  if "OPENAI_API" not in st.session_state:
    st.session_state["OPENAI_API"] = "" # 사용자가 입력한 OpenAI API를 저장하여 클라이언트 생성 시 사용

  if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": "You are a thoughtful assistan. Respond to all input in 25 words and answer in korea."}] # GPT API에 입력(input)으로 전달할 프롬프트 양식을 저장. 이전 질문과 답변 모두 차례로 누적하여 저장.

  if "check_audio" not in st.session_state:
    st.session_state["check_reset"] = False # 사용자가 리셋 버튼을 클릭한 상태를 나타내는 플래그로 해당 플래그가 True일 경우 사용자의 입력을 받기 전에 프로그램이 동작하는 것을 방지.

  ## 사이드바 생성  
  with st.sidebar:
    # OpenAI API Key 입력
    st.session_state["OPENAI_API"] = st.text_input(label="OPENAI API KEY", placeholder="Enter Your API Key", value="", type="password")
    
    st.markdown("---")
    
    # GPT모델 선택 버튼 생성
    model = st.radio(label="GPT Model", options=["gpt-4", "gpt-4o"])
    
    # 초기화 버튼 생성
    if st.button(label="Reset"):
      # 초기화 코드
      # 리셋 버튼을 누르면 기존 대화 내용을 모두 삭제하기 위해 st_session_state["chat"], st_session_state["message"], st_session_state["check_reset"]의 session_state를 초기화한다.
      st.session_state["chat"] = []
      st.session_state["messages"] = [{"role": "system", "content": "You are a thoughtful assistant. Respond to all input in 25 words and answer in korea."}]
      st.session_state["check_reset"] = True

  ## 기능 구현: 질문과 Chat-GPT의 답변을 아이폰의 문자 메세지 형태로 볼 수 있도록 구현한다.
  col1, col2 = st.colums(2)
  with col1:
    # 왼쪽 영역 작성
    st.subheader("질문")
    # 음성 녹음 아이콘 추가: "클릭하여 녹음하기" 버튼이 생성되고 해당 버튼을 클릭하면 "녹음 중..." 텍스트를 표시. 녹음파일은 array 형태로 audio라는 변수에 저장.
    audio = audiorecorder("클릭하여 녹음하기", "녹음 중...")
    # audio.duration_seconds > 0: audio.duration_seconds는 음성 녹음의 시간을 초 단위로 나타낸다. 음성 녹음이 실행되면 0보다 커져서 후속 단계를 진행한다.
    # and 사용자가 리셋 버튼을 누른 상태인지 확인한다.
    if (audio.duration_seconds > 0) and (st.session_state["check_reset"] == False):
      # 음성 재생
      st.audio(audio.export().read())
      # 음원 파일에서 텍스트 추출
      question = STT(audio, st.session_state["OPENAI_API"])
      
      # 채팅을 시각화하기 위해 질문 내용 저장
      now = datetime.now().strftime("%H:%M")
      st.session_state["chat"] = st.session_state["chat"]+[("user", now, question)]
      # GPT 모델에 넣을 프롬프트를 위해 질문 내용 저장
      st.session_state["message"] = st.session_state["message"]+[{"role": "user", "content": question}]

  with col2:
    # 오른쪽 영역 작성
    st.subheader("답변")
      
if __name__=="__main__":
  main()