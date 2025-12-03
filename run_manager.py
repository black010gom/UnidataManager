import os
import subprocess
import sys

# 경로 설정
BASE_DIR = os.path.dirname(__file__)
VENV_PYTHON = os.path.join(BASE_DIR, "p311venc2025", "Scripts", "python.exe")
C_DIR = os.path.join(BASE_DIR, "kivyC")
UI_DIR = os.path.join(BASE_DIR, "kivyUI")
C_FILE = os.path.join(C_DIR, "UnidataManager.c")
DLL_FILE = os.path.join(C_DIR, "UnidataManager.dll")
UI_FILE = os.path.join(UI_DIR, "UnidataManager.py")

# 1. 가상환경 활성화 + 라이브러리 설치
print("🔧 라이브러리 설치 중...")
subprocess.run([VENV_PYTHON, "-m", "pip", "install", "--upgrade", "pip", "wheel", "setuptools"])
subprocess.run([VENV_PYTHON, "-m", "pip", "install", "kivy", "pandas", "openpyxl"])

# 2. C 모듈 빌드
if not os.path.exists(DLL_FILE):
    print("⚙️ C 모듈 빌드 중...")
    subprocess.run(["gcc", "-shared", "-o", DLL_FILE, C_FILE], check=True)
else:
    print("✅ C DLL 이미 존재: 생략")

# 3. Kivy UI 실행
print("🚀 Kivy UI 실행 중...")
subprocess.run([VENV_PYTHON, UI_FILE])
