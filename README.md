# keyroot_community

# 개발 환경 및 기술 스택

### 백엔드
- **언어**: Python 3.x
- **프레임워크**: Flask 2.3.3
- **데이터베이스**: SQLite 
- **웹 서버**:Nginx

### 프론트엔드
- **마크업**: HTML5
- **스타일링**: CSS3 (커스텀 다크 테마)
- **스크립트**: JavaScript (바닐라)
- **템플릿 엔진**: Jinja2 (Flask 기본)

### 개발 도구
- **에디터**: 텍스트 에디터
- **버전 관리**: 로컬 개발
- **패키지 관리**: pip (Python)

## 프로젝트 구조 설계

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
│   └── admin.html        # 관리자 패널
