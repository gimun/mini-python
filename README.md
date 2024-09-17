# Mini Python

## 프로젝트 개요

이 프로젝트는 파이썬을 기반으로 개발되었으며, 패키지 의존성 관리를 위해 `venv`와 `requirements.txt`를 사용합니다.

## 프로젝트 구성

### 1. 가상환경 설정

이 프로젝트는 가상환경(Virtual Environment)을 사용하여 의존성을 관리합니다. 다음 단계를 따라 가상환경을 설정하고 패키지를 설치할 수 있습니다.

#### 1.1. 가상환경 생성

프로젝트 폴더 내에서 다음 명령어를 실행하여 가상환경을 생성합니다:

```bash
python -m venv venv
```

### 주요 내용:

1. **가상환경 설정**: `venv`를 사용하여 가상환경을 생성하고 활성화하는 방법 설명.
2. **패키지 설치**: `pip install -r requirements.txt` 명령어를 사용하여 의존성을 설치하는 방법 설명.
3. **가상환경 종료**: `deactivate` 명령어로 가상환경을 종료하는 방법 포함.
4. **프로젝트 실행**: 메인 스크립트를 실행하여 프로젝트를 시작하는 방법.

이 구성을 통해 프로젝트에 참여하는 개발자들이 쉽게 환경을 설정하고 프로젝트를 실행할 수 있게 됩니다.

## 초기 설정

- **`프로젝트 폴더에서 명령어 실행`**: Windows 기준
    - **가상환경 생성**:
      ```bash
      python -m venv venv
      ```
    - **가상환경 활성화**:
      ```bash
      venv\Scripts\activate
      ```
    - **필요한 패키지 설치**:
      ```bash
      pip install -r requirements.txt
      ```
    - **불필요한 패키지 제거 (선택 사항)**:
      ```bash
      pip uninstall pyproject-metadata meson meson-python
      ```
    - **설치된 패키지 확인**:
      ```bash
      pip freeze
      ```
    - **프로젝트 실행**:
      ```bash
      python <main_script.py>
      ```

## Venv 명령어 및 사용법

- **`Virtual Environment`**: 파이썬을 위한 가상 환경 생성 도구
    - **가상환경 비활성화**:
      ```bash
      deactivate
      ```
    - **패키지 설치**:
      ```bash
      pip install <package_name>
      ```
    - **설치된 패키지 목록 확인**:
      ```bash
      pip list
      ```

## requirements.txt

- **`프로젝트의 의존성을 관리`**: 프로젝트에 필요한 Python 패키지 목록이 기록된 파일
    - **설치된 패키지 저장**:
      ```bash
      pip freeze > requirements.txt
      ```
    - **필요한 패키지 설치**:
      ```bash
      pip install -r requirements.txt
      ```

