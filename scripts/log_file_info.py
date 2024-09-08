import os


def log_current_directory_and_files():
    """
    현재 작업 디렉토리와 해당 디렉토리에 있는 파일 목록을 로그로 출력하는 함수.
    """
    # 현재 작업 디렉토리 확인
    current_directory = os.getcwd()
    print(f"현재 작업 디렉토리: {current_directory}")

    # 현재 디렉토리 내 파일 및 폴더 목록 확인
    files_and_dirs = os.listdir(current_directory)
    print("\n현재 디렉토리에 있는 파일 및 폴더 목록:")
    for item in files_and_dirs:
        print(f"- {item}")

    """
    현재 파이썬 파일의 절대 경로를 출력하는 함수.
    """
    # 현재 실행 중인 파일의 절대 경로 확인
    absolute_path = os.path.abspath(__file__)
    print(f"현재 실행 중인 파일의 절대 경로: {absolute_path}")


if __name__ == "__main__":
    log_current_directory_and_files()
