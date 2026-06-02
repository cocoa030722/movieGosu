# 캐릭터:정보 대응표
char_table = {
    "메탄":{
        "jpn_name":"四国めたん",
        "text_color":"red",
        "position":("left", "bottom"),
        "size":0.2
    },
    "츠무기":{
        "jpn_name":"春日部つむぎ",
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
SCRIPT_FILE = "example.txt"  # 스크립트 파일
VIDEO_SIZE = (1280, 720)  # 해상도
FONT = "font/standardKOR.ttf"  # 텍스트 폰트
FONT_SIZE = 40
TEXT_COLOR = "white"

# 배경 파일(전역변수로 취급해 구현)
BGM_FILE = "Usagi Flap.mp3"
BACKGROUND_FILE = "background1.webp"
