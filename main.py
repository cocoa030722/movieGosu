import os

from numpy import char
from script_spliter import spliter
from filesort import file_sort
from effect import audio_effect, highlight

from lark import Lark, Transformer

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




# Lark 문법 정의
grammar = r"""
    start: (config | dialogue | comment)*

    config: "#" VAR ":" VALUE
    dialogue: CHARACTER "-" EMOTION ":" TEXT ":" EFFECT

    comment: /\/\/[^\n]*/  -> ignore_comment

    CHARACTER: /[a-zA-Z가-힣0-9_]+/
    EMOTION: /[a-zA-Z가-힣0-9_]+/
    TEXT: /[^:\n]+/
    EFFECT: /[^:\n]+/
    VAR: /[a-zA-Z가-힣0-9_]+/
    VALUE: /[^:\n]+/

    %import common.WS
    %ignore WS
"""

# Transformer를 사용하여 파싱된 트리를 변환
class ScriptTransformer(Transformer):
    def config(self, items):
        var, value = items
        return {"type": "config", "var": var, "value": value}

    def dialogue(self, items):
        character, emotion, text, effect = items
        return {"type": "dialogue", "character": character, "emotion": emotion, "text": text, "effect": effect}

    def ignore_comment(self, _):
        return None  # 주석 무시



def parse_script(script_file):
    """스크립트 파일을 읽어 블록 요소와 스크립트 줄을 분리"""
    with open(script_file, "r", encoding="utf-8") as file:
        lines = file.readlines()
        
    script_lines = []
    
    for line in lines:
        line = line.strip()
        if line:
            if line.startswith("//"): # 주석->무시함
                pass
            elif line.startswith("#"): # 블록 요소 처리
                script_lines.append({"block":line[1:].strip()})  # # 제거하고 저장
            else:
                character, dialogue, effect = line.split(":", 2)
                script_lines.append({"line":(character, dialogue, effect)})
    
    return script_lines

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

    # 파서 생성
    parser = Lark(grammar, start="start", parser="lalr", transformer=ScriptTransformer())

    # 테스트 입력
    with open(SCRIPT_FILE, "r", encoding="utf-8") as file:
        raw_script = file.read()

    print(raw_script)
    
    # 파싱 실행
    parsed_data = parser.parse(raw_script)

    # vktldgks ahems xhzmsdmf cnffur 출력
    print(parsed_data)
    '''
    # 스크립트 파일 읽기
    script = parse_script(SCRIPT_FILE)
    print(script)
    
    final_clips = []
    line_count = 1

    for line in script:
        print(line)
        if "block" in line.keys():
            global BGM_FILE
            global BACKGROUND_FILE
            token = line["block"].split(":")
            if token[0] == "bgm":
                BGM_FILE = token[1]
            elif token[0] == "background":
                BACKGROUND_FILE = token[1]
                
        elif "line" in line.keys():
            character, dialogue, effect = line["line"]
            char_line_path = os.path.join(LINE_DIR, f"{line_count:04d}.wav") if dialogue != "None" else None
            if dialogue != "None":
                line_count += 1
        
                char_image_path = os.path.join(CHARACTER_DIR, f"{character}.png") if character != "None" else None
        
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
    '''
    
if __name__ == "__main__":
    command = input("1.영상 제작 2.스크립트 대사 분리 3.파일 정렬")
    if command == "1":
        main()
    elif command == "2":
        spliter("example.txt", "output.txt")
    elif command == "3":
        file_sort()