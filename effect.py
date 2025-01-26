from moviepy import TextClip, AudioFileClip

def highlight(color:str, text:str, scene_duration) -> TextClip:
    text = text.replace("\\n", "\n")
    
    # TextClip 생성
    text_clip = TextClip(
        text=text,
        font="font/font.ttf",
        font_size=30,
        color=color,
        bg_color="black",
        size=(600, None),  # 가로 600px, 세로는 자동 조정
        method="label",
).with_duration(scene_duration).with_position("center")
    
    return text_clip

def audio_effect(dir:str) -> AudioFileClip:
    audio_effect = AudioFileClip(dir)
    return audio_effect