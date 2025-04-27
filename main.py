import os
import re

from numpy import char
from script_spliter import spliter
from filesort import file_sort
from effect import audio_effect, highlight

from moviepy import *

# 캐릭터:정보 대응표
char_table = {
    "메탄":{
        "text_color":"red",
        "position":("left", "bottom"),
        "size":0.2
    },
    "츠무기":{
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
AUDIO_EFFECT_DIR = "./audio/effect"  # 음향효과 디렉토리
CHARACTER_DIR = "./images/character"  # 캐릭터 이미지 디렉토리
BACKGROUND_DIR = "./images/background"  # 배경 이미지 디렉토리
OUTPUT_DIR = "./output"  # 출력 디렉토리
SCRIPT_FILE = "./example_short.txt"  # 스크립트 파일

# 기본 설정
VIDEO_SIZE = (1280, 720)  # 해상도
FONT = "font/standardKOR.ttf"  # 텍스트 폰트
FONT_SIZE = 40
TEXT_COLOR = "white"

# 배경 파일(전역변수로 취급해 구현)
BGM_FILE = "Usagi Flap.mp3"
BACKGROUND_FILE = "background1.webp"

# bgm의 시작 지점을 기록하는 변수
bgm_start = 0

def parse_script() -> list[dict]:
    # 정규 표현식 패턴 정의
    comment_pattern = re.compile(r"^\s*//")  # 주석
    config_pattern = re.compile(r"^\s*#\s*(\w+)\s*:\s*(.+)")  # 설정 변수
    dialogue_pattern = re.compile(r"^\s*([\w가-힣]+)-([\w가-힣]+):(.+):(.+)")  # 대사
    
    parsed_data = []

    with open(SCRIPT_FILE, "r", encoding="utf-8") as file:
        lines = file.readlines()
    
    for line in lines:  # 스크립트를 줄 단위로 읽음
        line = line.strip()  # 공백 제거

        if not line or comment_pattern.match(line):  
            continue  # 빈 줄 또는 주석이면 무시

        # 설정 변수 파싱
        config_match = config_pattern.match(line)
        if config_match:
            var, value = config_match.groups()
            parsed_data.append({"type": "config", "var": var, "value": value})
            continue

        # 대사 파싱
        dialogue_match = dialogue_pattern.match(line)
        if dialogue_match:
            character, emotion, text, effect = dialogue_match.groups()
            parsed_data.append({
                "type": "dialogue",
                "character": character,
                "emotion": emotion,
                "text": text.strip(),
                "effect": effect.strip()
            })
            continue

        # 규칙에 맞지 않는 경우 오류 출력
        print(f"Warning: '{line}'은(는) 인식할 수 없는 형식입니다.")

    return parsed_data
def create_clip(character=None, effect=None, dialogue=None, char_line_path=None, char_image_path=None, **kwargs):
    """캐릭터 이미지와 대사를 사용하여 개별 클립 생성"""
    
    video_clip = []
    audio_clip = []

    # 음성 파일 로드
    char_line_clip = AudioFileClip(char_line_path).with_effects([afx.MultiplyVolume(2.0)])
    audio_clip.append(char_line_clip)
    scene_duration = char_line_clip.duration

    # BGM
    global bgm_start
    bgm_dir = os.path.join(BGM_DIR, BGM_FILE)
    bgm_raw:AudioClip = AudioFileClip(bgm_dir).with_effects([afx.MultiplyVolume(0.1)])
    if bgm_start+scene_duration > bgm_raw.end:
        bgm_head = bgm_raw.subclipped(bgm_start, bgm_raw.end)
        tail_pointer = (bgm_start+scene_duration)-(bgm_raw.end)
        bgm_tail = bgm_raw.subclipped(0, tail_pointer)
        bgm_start = tail_pointer
        bgm = concatenate_audioclips([bgm_head, bgm_tail])
    else:
        bgm = bgm_raw.subclipped(bgm_start, bgm_start+scene_duration)
        bgm_start += scene_duration
    audio_clip.append(bgm)

    # 배경
    back_path = os.path.join(BACKGROUND_DIR, BACKGROUND_FILE)
    background_clip = ImageClip(img=back_path, duration=scene_duration).resized(VIDEO_SIZE)
    video_clip.append(background_clip)

    # 캐릭터 이미지 로드
    character = character.split("-")[0]
    image_clip = (ImageClip(img=char_image_path, duration=scene_duration)
                  .resized(char_table[character]["size"]).with_position(char_table[character]["position"]))
    video_clip.append(image_clip)

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
    video_clip.append(text_clip)

    # 효과 적용
    effect = effect.split("/")
    if effect[0] == "highlight":
        effect_clip = highlight(effect[1].split("=")[1], effect[2], scene_duration)
        video_clip.append(effect_clip)
    elif effect[0] == "audio_effect":
        effect_path = os.path.join(AUDIO_EFFECT_DIR, effect[1])
        effect_clip = audio_effect(effect_path)
        audio_clip.append(effect_clip)

    # 대사+BGM 결합
    composite_audio = CompositeAudioClip(audio_clip)

    # 비디오 클립에 텍스트와 음성을 결합
    final_clip = CompositeVideoClip(video_clip)
    final_clip = final_clip.with_audio(composite_audio)

    return final_clip

def main():
    """메인 함수: 스크립트를 읽고 영상을 생성"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 파싱 실행
    parsed_output = parse_script()
    print(parsed_output)
    
    final_clips = []
    line_count = 1

    for line in parsed_output:
        print(line)
        if line["type"] == "config":
            global BGM_FILE
            global BACKGROUND_FILE
            global bgm_start
            
            if line["var"] == "bgm":
                BGM_FILE = line["value"]
                bgm_start = 0
            elif line["var"] == "background":
                BACKGROUND_FILE = line["value"]
                
        elif line["type"] == "dialogue":
            
            character = line["character"]
            dialogue = line["text"]
            emotion = line["emotion"]
            effect = line["effect"]
            
            char_line_path = os.path.join(LINE_DIR, f"{line_count:04d}.wav") if dialogue != "None" or dialogue != "" else None
            if dialogue != "None" or dialogue != "":
                line_count += 1
                if os.path.exists(os.path.join(CHARACTER_DIR, f"{character}-{emotion}.png")):
                    char_image_path = os.path.join(CHARACTER_DIR, f"{character}-{emotion}.png") if character != "None" else None
                else:
                    char_image_path = os.path.join(CHARACTER_DIR, f"{character}-기본.png") if character != "None" else None
        
                clip = create_clip(character=character,
                                 effect=effect,
                                 dialogue=dialogue,
                                 char_line_path=char_line_path if char_line_path is not None else None,
                                 char_image_path=char_image_path if char_image_path is not None else None)
        
                final_clips.append(clip)
                print(f"클립 {len(final_clips)} 생성 완료")
        
            if final_clips:
                final_video = concatenate_videoclips(final_clips)
            else:
                raise Exception("No valid video clips found to concatenate")

    # 최종 영상 저장
    output_path = os.path.join(OUTPUT_DIR, "final_video.mp4")
    final_video.write_videofile(output_path, fps=24)

    # 메모리 정리
    for clip in final_clips:
        clip.close()

    print(f"최종 동영상 생성 완료: {output_path}")
    
    
if __name__ == "__main__":
    command = input("1.영상 제작 2.스크립트 대사 분리 3.파일 정렬")
    if command == "1":
        main()
    elif command == "2":
        spliter("example.txt", "output.txt")
    elif command == "3":
        file_sort()