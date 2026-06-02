# movieGosu

텍스트 스크립트를 읽어 캐릭터 대사·이미지·BGM을 자동으로 합성해 MP4 영상을 생성하는 Python 자동화 도구입니다.

## 동작 흐름

```
스크립트 파일 (.txt)
  └─ parse_script()       # 줄 단위 파싱 → Config / Dialogue 객체
       └─ line.act()      # 각 객체를 영상 클립으로 변환
            └─ create_clip()  # 배경 + 캐릭터 이미지 + 자막 + 음성 합성
  └─ concatenate_videoclips() + BGM 합성
       └─ final_video.mp4
```

## 프로젝트 구조

```
movieGosu/
├── main.py                         # 진입점 (영상 제작 / 스크립트 규격화)
├── line.py                         # Config·Dialogue 클래스 정의
├── config.py                       # 경로·캐릭터 설정 전역 상수
├── example.txt                     # 스크립트 예시 파일
├── output.txt                      # 규격화 출력 결과 (VOICEVOX 입력용)
├── spec.txt                        # 스크립트 형식 명세
├── todo.txt                        # 개발 메모
├── module/
│   ├── parse_script.py             # 스크립트 파서 (정규식 기반)
│   ├── create_clip.py              # 개별 클립 생성
│   ├── effect.py                   # highlight / audio_effect 효과
│   └── script_standardization.py  # 대사 추출 + 한→일 번역 (GoogleTranslator)
├── audio/
│   ├── raw_voice/                  # VOICEVOX 생성 음성 파일 (000_캐릭터명_*.wav)
│   ├── bgm/                        # BGM 파일
│   └── effect/                     # 음향 효과 파일
├── images/
│   ├── character/                  # 캐릭터 이미지 (캐릭터명-감정.png)
│   └── background/                 # 배경 이미지
└── font/
    └── standardKOR.ttf             # 자막 폰트
```

## 스크립트 형식

```
// scene 1                          ← 주석 (무시됨)
# background:background1.webp      ← 배경 설정
# bgm:Usagi Flap.mp3               ← BGM 설정

캐릭터-감정:대사:효과
```

**대사 줄 예시**

| 예시 | 설명 |
|------|------|
| `메탄-기본:안녕!:none` | 효과 없음 |
| `메탄-기본:설명:highlight/red/내용\n두번째줄` | 화면 중앙에 텍스트 박스 표시 |
| `메탄-기본:효과음:audio_effect/boom.mp3` | 음향 효과 추가 |

## 지원 캐릭터 (config.py)

| 이름 | VOICEVOX 캐릭터 | 자막 색상 | 위치 |
|------|----------------|-----------|------|
| 메탄 | 四国めたん | red | 좌하단 |
| 츠무기 | 春日部つむぎ | green | 우하단 |
| Narrator | — | green | 우하단 |

## 사용법

### 1. 음성 파일 준비 (VOICEVOX 워크플로)

```
# 스크립트에서 대사만 추출하고 한→일 번역
python main.py
> 2   ← "스크립트 대사 분리" 선택
```

`output.txt`에 `캐릭터명(일본어),번역된 대사` 형식으로 저장됩니다.  
이 파일을 VOICEVOX에 입력해 `000_캐릭터명_*.wav` 형식으로 음성을 생성한 뒤 `audio/raw_voice/`에 배치합니다.

### 2. 영상 제작

```
python main.py
> 1   ← "영상 제작" 선택
```

`output/final_video.mp4`로 최종 영상이 저장됩니다.

## 환경 구성

### Python 버전 요구사항

moviepy 2.x는 **Python 3.9–3.11** 을 공식 지원합니다.  
Python 3.12 이상(특히 3.14)에서는 의존 패키지 빌드 실패로 설치가 불가능합니다.

| 항목 | 권장 버전 |
|------|-----------|
| Python | **3.11.x** |
| moviepy | 2.2.1 |
| deep-translator | 1.11.4 |

> ffmpeg는 별도 설치 또는 PATH 등록이 필요합니다. moviepy가 내부적으로 `imageio-ffmpeg`를 번들로 포함하므로 일반적으로 별도 설치 없이 동작합니다. 단, 시스템 ffmpeg가 PATH에 있으면 그쪽을 우선 사용합니다.

---

### 설치 방법 (Python 3.11이 설치된 경우)

Python 3.11이 이미 있다면 가상환경을 만들어 의존성을 설치합니다.

**Windows (py launcher 사용)**
```bat
py -3.11 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

**macOS / Linux**
```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

실행 시에도 반드시 가상환경을 활성화한 상태에서 실행해야 합니다.

```bat
.venv\Scripts\activate
python main.py
```

---

### Python 3.11이 없는 경우 — 설치 방법

#### Windows

1. [python.org 다운로드 페이지](https://www.python.org/downloads/release/python-3119/)에서 **Python 3.11.x** Windows installer (64-bit) 다운로드
2. 설치 시 **"Add Python to PATH"** 체크
3. 설치 후 확인:
   ```bat
   py -3.11 --version
   ```
4. 위의 가상환경 설치 절차 진행

#### macOS

```bash
brew install python@3.11
python3.11 -m venv .venv
```

#### Linux (Ubuntu/Debian)

```bash
sudo apt install python3.11 python3.11-venv
python3.11 -m venv .venv
```

---

### pyenv를 사용하는 경우 (선택)

시스템에 여러 Python 버전이 혼재하는 경우 pyenv로 버전을 고정할 수 있습니다.

```bash
pyenv install 3.11.9
pyenv local 3.11.9
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 설정 변경 (config.py)

| 항목 | 기본값 | 설명 |
|------|--------|------|
| `VIDEO_SIZE` | `(1280, 720)` | 출력 해상도 |
| `FONT` | `font/standardKOR.ttf` | 자막 폰트 |
| `FONT_SIZE` | `40` | 자막 크기 |
| `SCRIPT_FILE` | `example.txt` | 입력 스크립트 |
| `OUTPUT_DIR` | `./output` | 출력 디렉토리 |

## 음성 파일 네이밍 규칙

`audio/raw_voice/` 안의 파일은 반드시 다음 형식을 따라야 합니다.

```
{3자리 순번}_{VOICEVOX 캐릭터명(일본어)}_{임의 문자열}.wav
예) 001_四国めたん_0.wav
    002_春日部つむぎ_0.wav
```

순번은 스크립트의 대사 순서와 일치해야 합니다.
