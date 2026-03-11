# keyroot_community

# 개발 환경 및 기술 스택

### 백엔드
- **언어**: Python 3.x
- **프레임워크**: Flask 2.3.3
- **데이터베이스**: SQLite 
- **웹 서버**:Nginx

### 프론트엔드
- **마크업**: HTML5
- **스타일링**: CSS3 
- **스크립트**: JavaScript
- **템플릿 엔진**: Jinja2 

### 개발 도구
- **에디터**: VScode
- **버전 관리**: 로컬 개발
- **패키지 관리**: pip (Python)

## 프로젝트 구조

```
keyroot_community/
├── app.py                 # Flask 메인 애플리케이션
├── requirements.txt       # Python 의존성 목록
├── run.bat               # Windows 실행 스크립트
├── keyroot.db            # SQLite 데이터베이스 
├── static/
│   └── style.css         # CSS 스타일시트
├── templates/            # HTML 템플릿 폴더
│   ├── base.html         # 기본 레이아웃 템플릿
│   ├── index.html        # 메인 페이지
│   ├── about.html        # 소개 페이지
│   ├── login.html        # 로그인 페이지
│   ├── register.html     # 회원가입 페이지
│   ├── board.html        # 게시판 페이지
│   ├── write.html        # 글쓰기 페이지
│   ├── guestbook.html    # 방명록 페이지
│   ├── search.html       # 검색 결과 페이지
│   ├── admin.html        # 관리자 패널
│   └── change_password.html # 비밀번호 변경 페이지
├── indiscriminate use/   # 무차별 공격 도구 폴더
│   ├── indiscriminate use.py   # 무차별 공격 메인 스크립트
│   ├── indiscriminate use.bat  # 무차별 공격 실행 배치파일
│   ├── passwords.txt     # 패스워드 사전 파일
│   ├── usernames.txt     # 사용자명 사전 파일
│   └── server_config.txt # 대상 서버 설정 파일
└── 우분투 자동스크립트/    # Ubuntu 자동 배포 스크립트
    ├── deploy.sh         # 자동 배포 스크립트
    ├── keyroot.service   # systemd 서비스 파일
    ├── nginx_config.conf # Nginx 설정 파일
    ├── requirements_ubuntu.txt # Ubuntu용 의존성
    └── wsgi.py          # WSGI 애플리케이션 엔트리포인트
```

## Windows 실행 방법
   ```bash
   run.bat
   ```

### Ubuntu/Linux 자동 배포
1. 우분투 자동스크립트 폴더로 이동:
   ```bash
   cd "우분투 자동스크립트"
   ```

2. 배포 스크립트 실행 권한 부여:
   ```bash
   chmod +x deploy.sh
   ```

3. 자동 배포 실행:
   ```bash
   sudo ./deploy.sh
   ```

4. 배포 완료 후 서버 IP로 접속
