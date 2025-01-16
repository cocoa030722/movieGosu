import os


# 파일 이름을 정렬하고 이름을 바꾸는 함수
def rename_files_in_directory(directory_path):
    # 디렉토리 안의 모든 파일 가져오기
    file_list = os.listdir(directory_path)

    # 파일을 사전순으로 정렬
    sorted_files = sorted(file_list)

    # 파일 이름 변경
    for i, file_name in enumerate(sorted_files):
        # 파일의 확장자 가져오기
        _, file_extension = os.path.splitext(file_name)

        # 새 파일 이름 생성 (예: 0001.mp3)
        new_file_name = f"{i + 1:04d}{file_extension}"

        # 기존 파일의 전체 경로와 새 파일의 전체 경로 생성
        old_file_path = os.path.join(directory_path, file_name)
        new_file_path = os.path.join(directory_path, new_file_name)

        # 파일 이름 변경
        os.rename(old_file_path, new_file_path)
        print(f"Renamed: {old_file_path} -> {new_file_path}")


# 실행 예제
directory_path = "audio/line"  # 파일이 있는 디렉토리 경로를 설정
rename_files_in_directory(directory_path)
