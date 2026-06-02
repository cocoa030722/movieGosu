"""parse_script() 단위 테스트 — 실제 example.txt 사용"""
import pytest
from module.parse_script import parse_script
from line import Config, Dialogue


@pytest.fixture
def parsed():
    return parse_script()


def test_returns_non_empty_list(parsed):
    assert isinstance(parsed, list)
    assert len(parsed) > 0


def test_config_count(parsed):
    configs = [x for x in parsed if isinstance(x, Config)]
    assert len(configs) == 2


def test_config_background(parsed):
    bg = next(x for x in parsed if isinstance(x, Config) and x.var == "background")
    assert bg.value == "background1.webp"


def test_config_bgm(parsed):
    bgm = next(x for x in parsed if isinstance(x, Config) and x.var == "bgm")
    assert bgm.value == "Usagi Flap.mp3"


def test_dialogue_count(parsed):
    dialogues = [x for x in parsed if isinstance(x, Dialogue)]
    assert len(dialogues) == 4


def test_dialogue_fields(parsed):
    dialogues = [x for x in parsed if isinstance(x, Dialogue)]
    expected = [
        ("메탄",  "기본", "퀵 정렬은 우선 배열 원소 중에서 기준이 되는 피벗을 선택해.", "none"),
        ("츠무기", "기본", "그런데 그 피벗은 어떤 기준으로 정하는 거야?",              "none"),
        ("메탄",  "기본", "음... 적당히?",                                          "none"),
        ("츠무기", "기본", "뭐야 그게? 그렇게 대충 정해도 되는 거야?",                "none"),
    ]
    for dlg, (char, emotion, text, effect) in zip(dialogues, expected):
        assert dlg.character == char
        assert dlg.emotion   == emotion
        assert dlg.text      == text
        assert dlg.effect    == effect


def test_order_preserved(parsed):
    """Config 블록이 Dialogue 블록보다 앞에 온다."""
    first_dialogue_idx = next(i for i, x in enumerate(parsed) if isinstance(x, Dialogue))
    last_config_idx    = max(i for i, x in enumerate(parsed) if isinstance(x, Config))
    assert last_config_idx < first_dialogue_idx


def test_comments_and_blank_lines_ignored():
    """주석·빈 줄이 포함된 스크립트도 올바르게 파싱된다."""
    import tempfile, os
    from module.parse_script import parse_script as _parse

    script = (
        "// 이 줄은 주석\n"
        "\n"
        "# background:bg.webp\n"
        "메탄-기본:안녕!:none\n"
    )
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8",
                                     suffix=".txt", delete=False) as f:
        f.write(script)
        tmp_path = f.name

    import module.parse_script as ps_mod
    original = ps_mod.SCRIPT_FILE
    ps_mod.SCRIPT_FILE = tmp_path
    try:
        result = _parse()
    finally:
        ps_mod.SCRIPT_FILE = original
        os.unlink(tmp_path)

    assert len(result) == 2
    assert isinstance(result[0], Config)
    assert isinstance(result[1], Dialogue)
