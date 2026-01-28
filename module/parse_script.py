import re

from line import Line, Config, Dialogue
from config import SCRIPT_FILE


def parse_script() -> list[Line]:
    """"""
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
            parsed_data.append(Config(var=var, value=value))
            continue

        # 대사 파싱
        dialogue_match = dialogue_pattern.match(line)
        if dialogue_match:
            character, emotion, text, effect = dialogue_match.groups()
            parsed_data.append(Dialogue(
                character=character,
                emotion=emotion,
                text=text.strip(),
                effect=effect.strip()
            ))
            continue

        # 규칙에 맞지 않는 경우 오류 출력
        print(f"Warning: '{line}'은(는) 인식할 수 없는 형식입니다.")

    return parsed_data
