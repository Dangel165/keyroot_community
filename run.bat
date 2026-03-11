@echo off
chcp 65001 > nul
cls
color 0A
echo.
echo  ╔════════════════════════════════════════════════╗
echo  ║         Key Root 커뮤니티 웹사이트                      ║
echo  ╚════════════════════════════════════════════════╝
echo.

if not exist venv (
    echo  [*] 가상환경 생성 중...
    python -m venv venv
)

echo  [*] 가상환경 활성화 중...
call venv\Scripts\activate

echo  [*] 의존성 설치 중...
pip install -r requirements.txt -q

echo.
echo  [*] 웹사이트 시작 중...
echo  [*] 브라우저에서 http://localhost:5000 으로 접속하세요
echo.
echo  ════════════════════════════════════════════════
echo  종료하려면 Ctrl+C를 누르세요
echo  ════════════════════════════════════════════════
echo.

python app.py

pause