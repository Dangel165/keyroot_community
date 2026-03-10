#!/usr/bin/env python3
# WSGI 설정 파일 - Gunicorn과 Nginx 연동용

from app import app

if __name__ == "__main__":
    app.run()