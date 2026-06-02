"""통합 테스트 — 실제 에셋을 사용해 클립 생성까지 검증"""
import os
import pytest
import config
from line import Config, Dialogue
from module.parse_script import parse_script


# ── 에셋 존재 확인 ──────────────────────────────────────────────

def test_line_dir_exists():
    assert os.path.isdir(config.LINE_DIR), f"LINE_DIR 없음: {config.LINE_DIR}"


def test_voice_files_present():
    files = sorted(os.listdir(config.LINE_DIR))
    assert len(files) >= 4, "음성 파일이 4개 이상 있어야 합니다"


def test_voice_files_naming():
    """파일명이 4자리 숫자로 시작하는지 확인"""
    for fname in os.listdir(config.LINE_DIR):
        prefix = fname[:4]
        assert prefix.isdigit(), f"네이밍 규칙 위반: {fname}"


def test_character_images_exist():
    for char in ("메탄", "츠무기"):
        path = os.path.join(config.CHARACTER_DIR, f"{char}-기본.png")
        assert os.path.isfile(path), f"캐릭터 이미지 없음: {path}"


def test_background_exists():
    path = os.path.join(config.BACKGROUND_DIR, config.BACKGROUND_FILE)
    assert os.path.isfile(path), f"배경 이미지 없음: {path}"


def test_bgm_exists():
    path = os.path.join(config.BGM_DIR, config.BGM_FILE)
    assert os.path.isfile(path), f"BGM 파일 없음: {path}"


# ── Config.act() 동작 검증 ────────────────────────────────────

def test_config_act_sets_background():
    clip = Config("background", "back2.webp").act()
    assert config.BACKGROUND_FILE == "back2.webp"
    assert clip.duration == 0
    clip.close()


def test_config_act_sets_bgm():
    clip = Config("bgm", "GigaChad.mp3").act()
    assert config.BGM_FILE == "GigaChad.mp3"
    clip.close()


# ── Dialogue.act() — 클립 생성 통합 테스트 ───────────────────

@pytest.mark.parametrize("line_no,char,emotion,text", [
    (1, "메탄",  "기본", "퀵 정렬은 우선 배열 원소 중에서 기준이 되는 피벗을 선택해."),
    (2, "츠무기", "기본", "그런데 그 피벗은 어떤 기준으로 정하는 거야?"),
    (3, "메탄",  "기본", "음... 적당히?"),
    (4, "츠무기", "기본", "뭐야 그게? 그렇게 대충 정해도 되는 거야?"),
])
def test_dialogue_creates_clip(line_no, char, emotion, text):
    """각 대사 라인이 올바른 클립(양수 duration, 오디오 포함)을 생성한다."""
    import line as line_module
    line_module.line_count = line_no

    dlg = Dialogue(character=char, emotion=emotion, text=text, effect="none")
    clip = dlg.act()

    assert clip is not None
    assert clip.duration > 0
    assert clip.audio is not None
    clip.close()


# ── 전체 파이프라인 — 파싱 → 클립 생성 → 연결 ──────────────

def test_full_pipeline_concatenation():
    """example.txt 전체를 파싱해 클립을 만들고 concatenate까지 성공하는지 검증"""
    from moviepy import concatenate_videoclips

    parsed = parse_script()
    clips = [item.act() for item in parsed]

    # Config.act()가 반환하는 duration=0 클립을 제외
    valid_clips = [c for c in clips if c.duration > 0]
    assert len(valid_clips) == 4

    final = concatenate_videoclips(valid_clips)
    assert final.duration == sum(c.duration for c in valid_clips)

    for c in clips:
        c.close()
    final.close()
