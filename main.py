
# Lets import moviepy, lets also import numpy we will use it a some point
from moviepy import (
    VideoClip,
    VideoFileClip,
    ImageSequenceClip,
    ImageClip,
    TextClip,
    ColorClip,
    AudioFileClip,
    AudioClip,
    CompositeVideoClip,
)
from moviepy import *
import numpy as np


# 이미지와 오디오 불러오기
image_clip = ImageClip("placeholder/placeholder_white.png", duration=5)
audio_clip = AudioFileClip("placeholder/placeholder.mp3")

# 오디오 추가
video = image_clip.set_audio(audio_clip)

video.preview(fps=10)

# 저장
video.write_videofile("output.mp4", fps=10)
