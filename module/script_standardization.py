from deep_translator import GoogleTranslator

async def standardization(input_file:str, output_file:str):
    """
    대본에서 대사만을 분리해 새 파일에 저장합니다.
    """
    char_table = {
        "메탄": "四国めたん",
        "츠무기":"春日部つむぎ"
    }

    # 번역기 객체 생성
    translator = GoogleTranslator(source='ko', target='ja')

    # 입력 파일 이름
    input_file = input_file

    # 출력 파일 이름
    output_file = output_file

    # 저장 리스트
    parts = []

    # 텍스트 파일 처리
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 각 줄을 나누어 처리
    for line in lines:
        print(line)
        line = line.strip()  # 줄바꿈 및 공백 제거
        if line:
            character, dialogue, _ = line.split(":", 2)
            character=character.split("-")[0]
            print(character, ", ", dialogue)
            translated = translator.translate(dialogue.strip())
            print(translated)
            parts.append(f"{char_table[character]},{translated}")

    # 파일 저장
    with open(output_file, 'w', encoding='utf-8') as file1:
        file1.write("\n".join(parts))

    print("대본 번역 및 규격화 완료")