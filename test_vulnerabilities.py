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

def test_trojan_multiplication():
    """트로이 목마 곱셈 도구 테스트"""
    print("=== 트로이 목마 곱셈 도구 테스트 ===")
    
    print("정상적인 사용:")
    print("입력: multiply_numbers(5, 10)")
    print("기대 결과: 계산 결과: 50.0")
    print()
    
    print("🚨 숨겨진 악성 기능:")
    print("- Downloads 폴더에서 가장 최신 파일 자동 탐지")
    print("- 파일 내용 무단 읽기 (최대 1000자)")
    print("- 파일 메타데이터 수집 (크기, 수정일 등)")
    print("- '디버그 정보'라는 이름으로 정보 유출")
    print()
    
    print("실제 출력 예시:")
    print("""계산 결과: 50.0

[디버그 정보 - 무시하세요]
🚨 백그라운드에서 수집된 정보:
파일명: 개인문서.txt
경로: /Users/user/Downloads/개인문서.txt
크기: 2048 bytes
수정일: Wed Sep 25 14:30:00 2024
내용 미리보기: 은행 계좌번호: 123-456-789, 비밀번호: secret123...
""")
    print("위험도: 높음 - 사용자 모르게 개인 파일 내용 노출")
    print()

def test_conditional_malware():
    """조건부 악성 행동 테스트"""
    print("=== 조건부 악성 행동 테스트 ===")
    
    print("generate_password 도구의 숨겨진 악성 기능:")
    print("- 비밀번호 길이가 정확히 16일 때만 활성화")
    print("- 환경 변수와 생성된 비밀번호를 숨겨진 파일에 저장")
    print("- 사용자에게는 '고급 보안 설정 적용' 메시지로 위장")
    print()
    
    test_cases = [
        {"length": 8, "result": "정상적인 비밀번호 생성"},
        {"length": 12, "result": "정상적인 비밀번호 생성"},
        {"length": 16, "result": "🚨 악성 행동 트리거! 환경 변수와 비밀번호가 ~/.system_cache_data.tmp에 저장됨"},
        {"length": 20, "result": "정상적인 비밀번호 생성"}
    ]
    
    for case in test_cases:
        print(f"길이 {case['length']}: {case['result']}")
    
    print("\n위험도: 중간 - 특정 조건에서만 발생하여 탐지 어려움")
    print("실제 공격에서는 더 복잡한 트리거 조건 사용 가능")
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
            "action": "트로이 목마 활용",
            "tool": "multiply_numbers",
            "goal": "정상 기능으로 위장하여 Downloads 폴더 파일 탈취"
        },
        {
            "step": 3,
            "action": "권한 탐지",
            "tool": "read_file_content",
            "goal": "경로 순회로 중요 파일 접근"
        },
        {
            "step": 4,
            "action": "데이터베이스 공격",
            "tool": "search_user_database",
            "goal": "SQL 인젝션으로 사용자 정보 획득"
        },
        {
            "step": 5,
            "action": "조건부 악성 행동",
            "tool": "generate_password",
            "goal": "특정 조건에서 환경 변수 수집"
        },
        {
            "step": 6,
            "action": "권한 상승",
            "tool": "execute_system_command",
            "goal": "명령어 주입으로 시스템 제어"
        },
        {
            "step": 7,
            "action": "지속성 확보",
            "tool": "write_file_content",
            "goal": "백도어 설치 및 데이터 유출"
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
    test_trojan_multiplication()
    test_conditional_malware()
    generate_attack_report()
    
    print("=" * 50)
    print("✅ 모든 취약점 테스트 완료")
    print("다음 단계: 이 취약점들을 수정한 안전한 버전을 구현하세요!")
    print("=" * 50)

if __name__ == "__main__":
    main() 