@echo off
chcp 65001 > nul
cls
color 0D
echo.
echo  ╔════════════════════════════════════════════════╗
echo  ║    무차별 대입 공격 도구                                          ║
echo  ╚════════════════════════════════════════════════╝
echo.
echo  [*] 서버 주소는 server_config.txt에서 설정 가능
echo  [*] usernames.txt와 passwords.txt 파일 사용
echo.

REM 패키지 설치
python -c "import colorama, requests" 2>nul
if errorlevel 1 (
    echo  [*] 필요한 패키지 설치 중...
    pip install colorama requests -q
    echo.
)

REM 크랙 실행
python "indiscriminate use.py"

echo.
echo  ════════════════════════════════════════════════
pause
