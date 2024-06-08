import streamlit as st


##### main function #####
def main():
  st.set_page_config(
    page_title="voice_assistant",
    layout="wide"
    )

  st.header("voice assistant program")

  st.markdown("---")
  
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
    
  with st.sidebar:
    st.session_state["OPENAI_API"] = st.text_input(label="OPENAI API KEY", placeholder="Enter Your API Key", value="", type="password")
    st.markdown("---")
    model = 
    
if __name__=="__main__":
  main()