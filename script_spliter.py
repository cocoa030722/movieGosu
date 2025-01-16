
def spliter(input_file:str, output_file:str):
    """
    대본에서 대사만을 분리해 새 파일에 저장합니다.
    """
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
            _, dialogue, _ = line.split(":", 2)
            parts.append(dialogue.strip())

    # 파일 저장
    with open(output_file, 'w', encoding='utf-8') as file1:
        file1.write("\n".join(parts))

    print("대본에서 대사를 분리했습니다.")