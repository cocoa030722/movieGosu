from gtts import gTTS

# 텍스트 기반 음성 생성
text = "Germany calling, germany calling..."
language = 'en'
tts = gTTS(text=text, lang=language)

# 파일 저장
tts.save("placeholder.mp3")