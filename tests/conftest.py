import os
import sys
import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 프로젝트 루트를 sys.path에 추가 (module/, line.py 등 임포트용)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


@pytest.fixture(autouse=True)
def reset_state():
    """각 테스트 전후로 전역 상태와 작업 디렉토리를 초기화한다."""
    original_cwd = os.getcwd()
    os.chdir(PROJECT_ROOT)

    import line as line_module
    import config
    line_module.line_count = 1
    config.BACKGROUND_FILE = "background1.webp"
    config.BGM_FILE = "Usagi Flap.mp3"

    yield

    line_module.line_count = 1
    os.chdir(original_cwd)
