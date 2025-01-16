import os
from script_spliter import spliter
from moviepy import *

# 캐릭터:정보 대응표
# TODO:"-" 단위 파싱-> 0번째 원소로 매칭
char_table = {
    "메탄-기본":{
        "text_color":"red",
        "position":("left", "bottom"),
        "size":0.2
    },
    
    "츠무기-기본":{
        "text_color":"green",
        "position":("right", "bottom"),
        "size":0.2
    },
    "Narrator":{
        "text_color":"green",
        "position":("right", "bottom"),
        "size":0.2
    },
}

# 음성 파일 및 캐릭터 이미지 경로 설정
LINE_DIR = "./audio/line"  # 대사 파일 디렉토리
BGM_DIR = "./audio/bgm"  # bgm 파일 디렉토리
CHARACTER_DIR = "./images/character"  # 캐릭터 이미지 디렉토리
BACKGROUND_DIR = "./images/background"  # 배경 이미지 디렉토리
OUTPUT_DIR = "./output"  # 출력 디렉토리
SCRIPT_FILE = "./example_short.txt"  # 스크립트 파일

# 기본 설정
VIDEO_SIZE = (1280, 720)  # 해상도
FONT = "font/standardKOR.ttf"  # 텍스트 폰트
FONT_SIZE = 40
TEXT_COLOR = "white"

# 배경 파일(전역변수로 취금해 구현)
BACKGROUND_FILE = "background1.webp"
BGM_START = 0

def parse_script(script_file):
    """스크립트 파일을 읽어 캐릭터, 대사, 효과로 분리"""
    with open(script_file, "r", encoding="utf-8") as file:
        lines = file.readlines()
    parsed_lines = []
    for line in lines:
        line = line.strip()
        if line:
            character, dialogue, effect = line.split(":", 2)
            parsed_lines.append((character, dialogue, effect))
    return parsed_lines

def create_clip(character=None, effect=None, dialogue=None, char_line_path=None, char_image_path=None, **kwargs):
    """캐릭터 이미지와 대사를 사용하여 개별 클립 생성"""

    """
    대사 주도 개발:
    1.대사가 none이 아니라면 각 라인의 대사 파일을 최우선으로 읽어옴
    2.대사를 기반으로 배경사진->캐릭터->자막->bgm의 지속시간을 결정
    """
    # 음성 파일 로드
    char_line_clip = AudioFileClip(char_line_path)
    scene_duration = char_line_clip.duration

    # BGM
    global BGM_START
    bgm:AudioClip = AudioFileClip("./audio/bgm/Usagi Flap.mp3").subclipped(BGM_START, BGM_START+scene_duration).with_effects([afx.MultiplyVolume(0.3)])
    BGM_START += scene_duration
    print(bgm.start, bgm.end)
    # 대사+BGM 결합
    composite_audio = CompositeAudioClip([char_line_clip, bgm])

    # 배경
    back_path = os.path.join(BACKGROUND_DIR, BACKGROUND_FILE)
    background_clip = ImageClip(img=back_path, duration=scene_duration).resized(VIDEO_SIZE)

    # 캐릭터 이미지 로드
    image_clip = (ImageClip(img=char_image_path, duration=scene_duration)
                  .resized(char_table[character]["size"]).with_position(char_table[character]["position"]))

    # 대사 텍스트 클립 생성
    text_clip = TextClip(text=dialogue,
                         font=FONT,
                         font_size=FONT_SIZE,
                         color=char_table[character]["text_color"],
                         size=VIDEO_SIZE,
                         method='caption',
                         vertical_align="bottom",
                         margin=(0, 20),
                         stroke_color="white",
                         stroke_width=3)
    text_clip = text_clip.with_duration(scene_duration).with_position("bottom")


    # 효과 적용
    #effect = effect.split("/")
    """
    if effect[0] == "fadein":
        image_clip = fadein(image_clip, 1)
    elif effect[0] == "fadeout":
        image_clip = fadeout(image_clip, 1)
    """

    # 비디오 클립에 텍스트와 음성을 결합
    final_clip = CompositeVideoClip([background_clip, image_clip, text_clip])
    final_clip = final_clip.with_audio(composite_audio)

    return final_clip

def main():
    """메인 함수: 스크립트를 읽고 영상을 생성"""
    # 스크립트 파일 읽기
    script = parse_script(SCRIPT_FILE)

    clips = []
    line_count = 1
    bgm_start = 0
    for character, dialogue, effect in script:
        char_line_path = os.path.join(LINE_DIR, f"{line_count:04d}.wav") if dialogue != "None" else None
        if dialogue != "None":
            line_count += 1

        char_image_path = os.path.join(CHARACTER_DIR, f"{character}.png") if character != "None" else None

        clip = create_clip(character=character,
                            effect=effect,
                            dialogue=dialogue,
                            char_line_path=char_line_path if not None else None,
                            char_image_path=char_image_path if not None else None)

        clips.append(clip)

    # 모든 클립을 결합
    final_video = concatenate_videoclips(clips)

    # 출력 저장
    output_path = os.path.join(OUTPUT_DIR, "final_video.mp4")
    final_video.write_videofile(output_path, fps=24)
    print(f"동영상 생성 완료: {output_path}")

if __name__ == "__main__":
    command = input("1.영상 제작 2.스크립트 대사 분리")
    if command == "1":
        os.makedirs(OUTPUT_DIR, exist_ok=True)  # 출력 디렉토리 생성
        main()
    elif command == "2":
        spliter("example.txt", "output.txt")

