from gtts import gTTS

# gTTS 메소드의 text에 음성으로 변경할 텍스트를 입력하고, 변환할 언어를 선택한다.
tts = gTTS(text="Hello. I am learning voice assistant program.", lang="ko")
tts.save("output.mp3")

