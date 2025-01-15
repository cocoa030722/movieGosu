import os
from moviepy import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips, ImageClip, ColorClip

# 캐릭터:정보 대응표
char_table = {
    "CHARACTER_1":{
        "text_color":"red",
        "position":("left", "bottom")
    },
    
    "CHARACTER_2":{
        "text_color":"green",
        "position":("right", "bottom")
    }
}

# 음성 파일 및 캐릭터 이미지 경로 설정
AUDIO_DIR = "./audio"  # 음성 파일 디렉토리
IMAGE_DIR = "./images"  # 캐릭터 이미지 디렉토리
OUTPUT_DIR = "./output"  # 출력 디렉토리
SCRIPT_FILE = "./example.txt"  # 스크립트 파일

# 기본 설정
VIDEO_SIZE = (1280, 720)  # 해상도
FONT = "font/standardKOR.ttf"  # 텍스트 폰트
FONT_SIZE = 40
TEXT_COLOR = "white"

def parse_script(script_file):
    """스크립트 파일을 읽어 캐릭터, 효과, 대사로 분리"""
    with open(script_file, "r", encoding="utf-8") as file:
        lines = file.readlines()
    parsed_lines = []
    for line in lines:
        line = line.strip()
        if line:
            character, effect, dialogue = line.split(":", 2)
            parsed_lines.append((character, effect, dialogue))
    return parsed_lines

def create_clip(character, effect, dialogue, audio_path, image_path):
    """캐릭터 이미지와 대사를 사용하여 개별 클립 생성"""
    # 검은 배경 
    background_clip = ColorClip(size=VIDEO_SIZE, color=(0, 0, 0)).with_duration(5)
    
    # 캐릭터 이미지 로드
    image_clip = ImageClip(image_path).with_duration(background_clip.duration).with_position(char_table[character]["position"])

    # 대사 텍스트 클립 생성
    text_clip = TextClip(text=dialogue, font=FONT, font_size=FONT_SIZE,  color=char_table[character]["text_color"], size=VIDEO_SIZE, method='caption', stroke_color="white", stroke_width=3)
    text_clip = text_clip.with_duration(background_clip.duration).with_position("bottom")

    # 음성 파일 로드
    audio_clip = AudioFileClip(audio_path)

    # 효과 적용
    """
    if effect == "fadein":
        image_clip = fadein(image_clip, 1)
    elif effect == "fadeout":
        image_clip = fadeout(image_clip, 1)
    """
    # 비디오 클립에 텍스트와 음성을 결합
    final_clip = CompositeVideoClip([background_clip, image_clip, text_clip])
    final_clip = final_clip.with_audio(audio_clip)
    return final_clip

def main():
    """메인 함수: 스크립트를 읽고 영상을 생성"""
    # 스크립트 파일 읽기
    script = parse_script(SCRIPT_FILE)

    clips = []
    for character, effect, dialogue in script:
        audio_path = os.path.join(AUDIO_DIR, f"{character}.wav")  # 캐릭터 음성 파일
        image_path = os.path.join(IMAGE_DIR, f"{character}.png")  # 캐릭터 이미지 파일

        if os.path.exists(audio_path) and os.path.exists(image_path):
            clip = create_clip(character, effect, dialogue, audio_path, image_path)
            clips.append(clip)
        else:
            print(f"파일을 찾을 수 없습니다: {audio_path} 또는 {image_path}")
            print("그럼 죽어")
            exit()

    # 모든 클립을 결합
    final_video = concatenate_videoclips(clips)

    # 출력 저장
    output_path = os.path.join(OUTPUT_DIR, "final_video.mp4")
    final_video.write_videofile(output_path, fps=24)
    print(f"동영상 생성 완료: {output_path}")

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)  # 출력 디렉토리 생성
    main()

    """
# 배경 레이어 생성 (30초 지속)
background = ImageClip("background.webp").with_duration(30)

# 지역 레이어 생성 함수
def create_scene(image_path, audio_path, text, start_time, duration=3):
    # 인물 사진 (지역 씬의 배경)
    person_clip = ImageClip(image_path).with_duration(duration).with_position("center").with_layer_index(2)

    # 대사 오디오
    audio = AudioFileClip(audio_path).subclipped(0, duration)

    # 자막
    subtitle = TextClip(text=text,  font="Pretendard-Regular.ttf", font_size=50, color="white", bg_color="black")
    subtitle = subtitle.with_duration(duration).with_position(("center", "bottom")).with_layer_index(1)

    # 지역 씬 합치기
    scene = CompositeVideoClip([person_clip, subtitle]).with_audio(audio).with_start(start_time)
    return scene

# 지역 씬 생성
scenes = [
    create_scene("person1.webp", "audio1.mp3", "안녕하세요", start_time=0),
    create_scene("person2.png", "audio2.mp3", "반갑습니다", start_time=3),
    create_scene("person3.webp", "audio3.mp3", "다음 장면으로 넘어가겠습니다", start_time=6),
]

# 모든 지역 씬 연결
scene_layer = concatenate_videoclips(scenes)

# 지역 레이어와 배경 레이어 합치기
final_clip = CompositeVideoClip([background, scene_layer])

# 최종 비디오 저장
final_clip.write_videofile("output.mp4", fps=24)
    """