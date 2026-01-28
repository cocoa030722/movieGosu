import os

from moviepy import AudioFileClip, AudioClip, concatenate_audioclips, ImageClip, TextClip, CompositeAudioClip, \
    CompositeVideoClip
from moviepy.audio import fx

from config import char_table, BGM_DIR, AUDIO_EFFECT_DIR, BACKGROUND_DIR, VIDEO_SIZE, FONT, FONT_SIZE, BGM_FILE, \
    BACKGROUND_FILE
from module.effect import highlight, audio_effect

def create_clip(character=None, effect=None, dialogue=None, char_line_path=None, char_image_path=None, **kwargs):
    """캐릭터 이미지와 대사를 사용하여 개별 클립 생성"""
    """
    1.대사+캐릭터+배경을 조합한 각 씬을 생성
    2.개별 씬들을 조합
    3.통합된 영상에 bgm을 삽입
    """
    video_clip = []
    audio_clip = []

    # 음성 파일 로드
    char_line_clip = AudioFileClip(char_line_path).with_effects([fx.AudioNormalize(), fx.MultiplyVolume(1.0)])
    audio_clip.append(char_line_clip)
    # 씬의 길이는 대사 파일의 길이임
    scene_duration = char_line_clip.duration

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

    # 대사+음향 효과 결합
    composite_audio = CompositeAudioClip(audio_clip)

    # 비디오 클립에 텍스트와 음성을 결합
    final_clip = CompositeVideoClip(video_clip)
    final_clip = final_clip.with_audio(composite_audio)

    return final_clip
