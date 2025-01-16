# 입력 파일 이름
input_file = "input.txt"

# 출력 파일 이름
output_file_1 = "output.txt"

# 저장 리스트
front_parts = []

# 텍스트 파일 처리
with open(input_file, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 각 줄을 나누어 처리
for line in lines:
    print(line)
    line = line.strip()  # 줄바꿈 및 공백 제거
    if line:
        _, dialogue, _ = line.split(":", 2)
        front_parts.append(dialogue.strip())

# 파일 저장
with open(output_file_1, 'w', encoding='utf-8') as file1:
    file1.write("\n".join(front_parts))


print("파일에 저장되었습니다.")