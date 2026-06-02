import abc
import os

import config
from config import LINE_DIR, char_table, CHARACTER_DIR
from module.create_clip import create_clip
from moviepy import *

class Line(abc.ABC):
    @abc.abstractmethod
    def act(self):
        pass


class Config(Line):
    var: str
    value: str
    def __init__(self, var, value):
        self.var = var
        self.value = value

    def act(self):
        global bgm_start

        if self.var == "bgm":
            config.BGM_FILE = self.value
            bgm_start = 0
        elif self.var == "background":
            config.BACKGROUND_FILE = self.value
        return ColorClip(size=(1280, 720), color=(0, 0, 0), duration=0)

# 몇 번째 줄인지를 기록
line_count = 1

class Dialogue(Line):
    character: str
    emotion: str
    text: str
    effect: str
    def __init__(self, character, emotion, text, effect):
        self.character = character
        self.emotion = emotion
        self.text = text
        self.effect = effect

    def act(self):
        global line_count
        global final_clips

        # 조건에 맞는 파일 찾기
        for filename in os.listdir(LINE_DIR):
            if filename.startswith(f"{line_count:04d}"):
                char_line_path = os.path.join(LINE_DIR, filename)
                break
        else:
            raise FileNotFoundError(f"Line {line_count}에 대응하는 음성 파일을 찾을 수 없습니다.")

        if self.text != "": # 비어 있지 않을 시
            line_count += 1
            # 감정에 대응하는 파일이 있다면 사용, 없다면 기본값 사용
            if os.path.exists(os.path.join(CHARACTER_DIR, f"{self.character}-{self.emotion}.png")):
                char_image_path = os.path.join(CHARACTER_DIR,
                                               f"{self.character}-{self.emotion}.png") if self.character != "None" else None
            else:
                char_image_path = os.path.join(CHARACTER_DIR, f"{self.character}-기본.png") if self.character != "None" else None

            clip = create_clip(character=self.character,
                               effect=self.effect,
                               dialogue=self.text,
                               char_line_path=char_line_path,
                               char_image_path=char_image_path)
            return clip
