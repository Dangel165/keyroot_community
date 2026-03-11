from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# 데이터베이스 파일 경로
DATABASE = 'keyroot_community.db'

# 로그인 시도 추적 
LOGIN_ATTEMPTS = {}
MAX_ATTEMPTS = 5
LOCKOUT_DURATION = 300  

# XSS 방지 CSP 헤더
@app.after_request
def add_security_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self'; frame-src 'none'; object-src 'none';"
    return response

# 데이터 베이스는 AI로 짯습니다

# 데이터베이스 초기화 함수
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # 사용자 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT NOT NULL,
            created_at TEXT NOT NULL,
            is_admin BOOLEAN DEFAULT FALSE,
            updated_at TEXT
        )
    ''')
    
    # 게시글 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            author TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    
    # 방명록 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS guestbook (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    
    # 기본 관리자 계정 생성 
    cursor.execute("SELECT * FROM users WHERE username = ?", ('admin',))
    if not cursor.fetchone():
        admin_password = generate_password_hash('admin123')
        cursor.execute(
            "INSERT INTO users (username, password, email, created_at, is_admin, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
            ('admin', admin_password, 'admin@keyroot.com', datetime.now(), True, datetime.now())
        )
    
    conn.commit()
    conn.close()

# 메인 페이지
@app.route('/')
def index():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts ORDER BY created_at DESC LIMIT 5")
    posts = cursor.fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

# 소개 페이지
@app.route('/about')
def about():
    return render_template('about.html')

# 로그인 페이지 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        client_ip = request.remote_addr
        current_time = datetime.now()
        
        # IP 차단 확인
        if client_ip in LOGIN_ATTEMPTS:
            attempts = LOGIN_ATTEMPTS[client_ip]
            if 'locked_until' in attempts and attempts['locked_until'] > current_time:
                remaining = int((attempts['locked_until'] - current_time).total_seconds())
                flash(f'IP가 차단되었습니다. {remaining}초 후에 다시 시도하세요.')
                return render_template('login.html')
            
            # 차단 시간이 지났으면 초기화
            if 'locked_until' in attempts and attempts['locked_until'] <= current_time:
                del LOGIN_ATTEMPTS[client_ip]
        
        username = request.form['username']
        password = request.form['password']

        # 데이터베이스 연결
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        # 로그인 성공 시 세션 설정
        if user and check_password_hash(user[2], password):
            # 로그인 성공 시 시도 기록 초기화
            if client_ip in LOGIN_ATTEMPTS:
                del LOGIN_ATTEMPTS[client_ip]
                
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['is_admin'] = user[5]
            flash('로그인 성공!')
            return redirect(url_for('index'))
        else:
            # 로그인 실패 시 시도 횟수 증가
            if client_ip not in LOGIN_ATTEMPTS:
                LOGIN_ATTEMPTS[client_ip] = {'count': 0, 'first_attempt': current_time}
            
            LOGIN_ATTEMPTS[client_ip]['count'] += 1
            LOGIN_ATTEMPTS[client_ip]['last_attempt'] = current_time
            
            # 최대 시도 횟수 초과 시 IP 차단
            if LOGIN_ATTEMPTS[client_ip]['count'] >= MAX_ATTEMPTS:
                LOGIN_ATTEMPTS[client_ip]['locked_until'] = current_time + timedelta(seconds=LOCKOUT_DURATION)
                flash(f'너무 많은 로그인 실패로 IP가 {LOCKOUT_DURATION//60}분간 차단되었습니다.')
            else:
                remaining_attempts = MAX_ATTEMPTS - LOGIN_ATTEMPTS[client_ip]['count']
                flash(f'로그인 실패! 남은 시도 횟수: {remaining_attempts}')
            
            return render_template('login.html')

    return render_template('login.html')

# 회원가입 페이지
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        
        password_hash = generate_password_hash(password)
        
        # 데이터베이스에 사용자 추가
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password, email, created_at, is_admin, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                          (username, password_hash, email, datetime.now(), False, datetime.now()))
            conn.commit()
            flash('회원가입이 완료되었습니다!')
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('이미 존재하는 사용자명입니다.')
            conn.close()
            return render_template('register.html')

    return render_template('register.html')

# 패스워드 변경 페이지
@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'user_id' not in session:
        flash('로그인이 필요합니다.')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        if new_password != confirm_password:
            flash('새 패스워드가 일치하지 않습니다.')
            return render_template('change_password.html')
        
        # 현재 패스워드 확인
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE id = ?", (session['user_id'],))
        user = cursor.fetchone()
        
        if not user or not check_password_hash(user[0], current_password):
            flash('현재 패스워드가 올바르지 않습니다.')
            conn.close()
            return render_template('change_password.html')
        
        # 새 패스워드로 업데이트
        new_password_hash = generate_password_hash(new_password)
        cursor.execute("UPDATE users SET password = ?, updated_at = ? WHERE id = ?",
                      (new_password_hash, datetime.now(), session['user_id']))
        conn.commit()
        conn.close()
        
        flash('패스워드가 성공적으로 변경되었습니다.')
        return redirect(url_for('index'))
    
    return render_template('change_password.html')

# 로그아웃
@app.route('/logout')
def logout():
    session.clear()
    flash('로그아웃되었습니다.')
    return redirect(url_for('index'))

# 게시판 페이지
@app.route('/board')
def board():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts ORDER BY created_at DESC")
    posts = cursor.fetchall()
    conn.close()
    return render_template('board.html', posts=posts)

# 글쓰기 라우트
@app.route('/write', methods=['GET', 'POST'])
def write():
    if 'username' not in session:
        flash('로그인이 필요합니다.')
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        # 데이터베이스에 게시글 추가
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO posts (title, content, author, created_at) VALUES (?, ?, ?, ?)",
                      (title, content, session['username'], datetime.now()))
        conn.commit()
        conn.close()

        flash('게시글이 작성되었습니다!')
        return redirect(url_for('board'))

    return render_template('write.html')

# 방명록 페이지
@app.route('/guestbook', methods=['GET', 'POST'])
def guestbook():
    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']

        # 데이터베이스에 방명록 추가
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO guestbook (name, message, created_at) VALUES (?, ?, ?)",
                      (name, message, datetime.now()))
        conn.commit()
        conn.close()

        flash('방명록이 등록되었습니다!')
        return redirect(url_for('guestbook'))

    # 방명록 목록 조회
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM guestbook ORDER BY created_at DESC")
    entries = cursor.fetchall()
    conn.close()

    return render_template('guestbook.html', entries=entries)

# 검색 기능
@app.route('/search')
def search():
    query = request.args.get('q', '')
    if query:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM posts WHERE title LIKE ? OR content LIKE ? ORDER BY created_at DESC",
                      (f'%{query}%', f'%{query}%'))
        posts = cursor.fetchall()
        conn.close()
        return render_template('search.html', posts=posts, query=query)
    else:
        return render_template('search.html', posts=[], query='')

# 관리자 페이지
@app.route('/admin')
def admin():
    if 'username' not in session or not session.get('is_admin'):
        flash('관리자 권한이 필요합니다.')
        return redirect(url_for('login'))

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # 사용자 목록 조회
    cursor.execute("SELECT id, username, email, created_at, is_admin FROM users")
    users = cursor.fetchall()
    
    # 게시글 목록 조회
    cursor.execute("SELECT id, title, author, created_at FROM posts ORDER BY created_at DESC")
    posts = cursor.fetchall()
    
    conn.close()
    
    return render_template('admin.html', users=users, posts=posts)

# API: 사용자 목록 
@app.route('/api/users')
def api_users():
    if 'username' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 401

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email, created_at, is_admin FROM users")
    users = cursor.fetchall()
    conn.close()

    users_list = []
    for user in users:
        users_list.append({
            'id': user[0],
            'username': user[1],
            'email': user[2],
            'created_at': user[3],
            'is_admin': user[4]
        })

    return jsonify(users_list)

if __name__ == '__main__':
    # 데이터베이스 초기화
    init_db()
    
    # Flask 앱 실행
    app.run(debug=True, host='0.0.0.0', port=5000)