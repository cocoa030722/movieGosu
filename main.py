from moviepy import VideoClip, TextClip, CompositeVideoClip, ImageClip, VideoFileClip
from lark import Lark

# 텍스트 파일 읽기
with open("example.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

# 각 줄을 ':' 기준으로 모두 나누기
split_lines = [line.strip().split(':') for line in lines]

characters = []
effects = []
speaks = []

# 결과 출력
for items in split_lines:
    characters.append(items[0])
    effects.append(items[1])
    speaks.append(items[2])

def create_video_from_script(split_lines):
    clips = []  # 모든 장면을 저장할 리스트
    current_time = 0  # 현재 시간 추적
    
    for line in split_lines:
        if line[0] != "NONE":  # 캐릭터
            print(line[0])
            character = line[0]
            image_clip = (ImageClip(f"placeholder/{character}.png")
                         .set_start(current_time)
                         .set_duration(3))
            clips.append(image_clip)
            current_time += 3

        if line[1] != "NONE":  # 효과
            print(line[1])
            current_time += 3

        if line[2] != "NONE":  # 대사
            print(line[2])
            speak = line[2]
            text_clip = (TextClip(text=speak, font="font/font.ttf", 
                                font_size=20, color="black")
                        .set_start(current_time)
                        .set_duration(3))
            clips.append(text_clip)
            current_time += 3

    # 모든 클립을 연결
    final_video = CompositeVideoClip(clips, size=(1280, 720))
    return final_video

# 스크립트로 영상 생성
final_clip = create_video_from_script(split_lines)

# 결과 저장
final_clip.write_videofile("output_video.mp4", fps=24)
