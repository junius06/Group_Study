import streamlit as st


##### main function #####
def main():
  st.set_page_config(
    page_title="voice_assistant",
    layout="wide"
    )

  st.header("voice assistant program")

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
    st.session_state["chat"] = []

  if "OPENAI_API" not in st.session_state:
    st.session_state["OPENAI_API"] = ""

  if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": "You are a thoughtful assistan. Respond to all input in 25 words and answer in korea."}]

  if "check_audio" not in st.session_state:
    st.session_state["check_reset"] = False

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
      # st.experimental_rerun()
      st.session_state["chat"] = []
      st.session_state["messages"] = [{"role": "system", "content": "You are a thoughtful assistant. Respond to all input in 25 words and answer in korea."}]
      st.session_state["check_reset"] = True

  ## 기능 구현: 질문과 Chat-GPT의 답변을 아이폰의 문자 메세지 형태로 볼 수 있도록 구현한다.
  col1, col2 = st.colums(2)
  with col1:
    # 왼쪽 영역 작성
    st.subheader("질문")

  with col2:
    # 오른쪽 영역 작성
    st.subheader("답변")
      
if __name__=="__main__":
  main()