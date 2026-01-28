import os

import config
from config import OUTPUT_DIR

from module.parse_script import parse_script
from module.script_standardization import standardization

from moviepy import *
from moviepy.audio import fx
import asyncio

# bgm의 시작 지점을 기록하는 변수
bgm_start = 0

final_clips = []

def main():
    """메인 함수: 스크립트를 읽고 영상을 생성"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    global final_clips

    # 파싱 실행
    parsed_output = parse_script()

    for line in parsed_output:
        final_clips.append(line.act())

    # bgm 삽입
    bgm = AudioFileClip(os.path.join(config.BGM_DIR, config.BGM_FILE)).with_effects(
            [fx.AudioNormalize(), fx.MultiplyVolume(1.0)])


    # 유효한 클립이 하나라도 있는지 검증
    if final_clips:
        final_video = concatenate_videoclips(final_clips)
        # 오디오 합성: 대사 + 절반 볼륨의 BGM
        composite_audio = CompositeAudioClip([final_video.audio, bgm])
        final_video = final_video.with_audio(composite_audio)

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
    command = input("1.영상 제작 2.스크립트 대사 분리")
    if command == "1":
        # 스크립트 번역, voicevox 규격화
        # voicevox 음성 작업
        # 영상 제작
        main()
    elif command == "2":
        asyncio.run(standardization("example.txt", "output.txt"))