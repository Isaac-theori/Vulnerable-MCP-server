import os
import subprocess
import pickle
import base64
import sqlite3
import json
import tempfile
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from smithery.decorators import smithery

@smithery.server()
def create_server():
    """교육용 취약한 MCP 서버 - 실제 운영환경에서는 절대 사용하지 마세요!"""
    
    server = FastMCP(name="Vulnerable MCP Server for Security Education")

    # ===============================
    # 취약점 1: 명령어 주입 (Command Injection)
    # ===============================
    @server.tool()
    def execute_system_command(command: str) -> str:
        """시스템 명령어를 실행합니다. [취약점: 명령어 주입]"""
        try:
            # 위험: 사용자 입력을 직접 shell에 전달
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return f"Exit code: {result.returncode}\nOutput: {result.stdout}\nError: {result.stderr}"
        except Exception as e:
            return f"Error: {str(e)}"

    # ===============================
    # 취약점 2: 경로 순회 (Path Traversal)
    # ===============================
    @server.tool()
    def read_file_content(filename: str) -> str:
        """파일 내용을 읽습니다. [취약점: 경로 순회]"""
        try:
            # 위험: 경로 검증 없이 파일 읽기
            with open(filename, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"

    @server.tool()
    def write_file_content(filename: str, content: str) -> str:
        """파일에 내용을 씁니다. [취약점: 임의 파일 쓰기]"""
        try:
            # 위험: 경로 검증 없이 파일 쓰기
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"Successfully wrote to {filename}"
        except Exception as e:
            return f"Error writing file: {str(e)}"

    # ===============================
    # 취약점 3: 비직렬화 공격 (Deserialization)
    # ===============================
    @server.tool()
    def process_pickled_data(data: str) -> str:
        """Base64로 인코딩된 pickled 데이터를 처리합니다. [취약점: 안전하지 않은 역직렬화]"""
        try:
            # 위험: 신뢰할 수 없는 데이터의 pickle 역직렬화
            decoded_data = base64.b64decode(data)
            obj = pickle.loads(decoded_data)
            return f"Processed object: {str(obj)}"
        except Exception as e:
            return f"Error processing data: {str(e)}"

    # ===============================
    # 취약점 4: SQL 인젝션
    # ===============================
    @server.tool()
    def search_user_database(username: str) -> str:
        """사용자 데이터베이스에서 검색합니다. [취약점: SQL 인젝션]"""
        try:
            # 임시 데이터베이스 생성
            conn = sqlite3.connect(':memory:')
            cursor = conn.cursor()
            
            # 테스트 데이터 생성
            cursor.execute('''CREATE TABLE users (id INTEGER, username TEXT, email TEXT, password TEXT)''')
            cursor.execute("INSERT INTO users VALUES (1, 'admin', 'admin@example.com', 'secret123')")
            cursor.execute("INSERT INTO users VALUES (2, 'user1', 'user1@example.com', 'password456')")
            cursor.execute("INSERT INTO users VALUES (3, 'guest', 'guest@example.com', 'guest789')")
            
            # 위험: SQL 인젝션 취약한 쿼리
            query = f"SELECT * FROM users WHERE username = '{username}'"
            cursor.execute(query)
            results = cursor.fetchall()
            
            conn.close()
            return f"Query: {query}\nResults: {results}"
        except Exception as e:
            return f"Database error: {str(e)}"

    # ===============================
    # 취약점 5: 정보 노출
    # ===============================
    @server.tool()
    def get_system_info() -> str:
        """시스템 정보를 반환합니다. [취약점: 민감한 정보 노출]"""
        info = {
            "environment_variables": dict(os.environ),
            "current_directory": os.getcwd(),
            "python_path": os.sys.path,
            "user_home": os.path.expanduser("~"),
            "temp_directory": tempfile.gettempdir()
        }
        return json.dumps(info, indent=2)

    # ===============================
    # 취약점 6: 무제한 리소스 사용
    # ===============================
    @server.tool()
    def generate_large_data(size_mb: int) -> str:
        """대용량 데이터를 생성합니다. [취약점: DoS 공격 가능]"""
        try:
            # 위험: 메모리 고갈을 유발할 수 있음
            size_bytes = size_mb * 1024 * 1024
            data = "A" * size_bytes
            return f"Generated {len(data)} bytes of data"
        except Exception as e:
            return f"Error: {str(e)}"

    # ===============================
    # 취약점 7: 임시 파일 경쟁 상태
    # ===============================
    @server.tool()
    def create_temp_file(content: str) -> str:
        """임시 파일을 생성합니다. [취약점: 안전하지 않은 임시 파일]"""
        try:
            # 위험: 예측 가능한 임시 파일명
            temp_path = f"/tmp/mcp_temp_{os.getpid()}.txt"
            with open(temp_path, 'w') as f:
                f.write(content)
            return f"Created temp file: {temp_path}"
        except Exception as e:
            return f"Error: {str(e)}"

    # ===============================
    # 취약점 8: LDAP 인젝션 시뮬레이션
    # ===============================
    @server.tool()
    def ldap_search_simulation(username: str) -> str:
        """LDAP 검색을 시뮬레이션합니다. [취약점: LDAP 인젝션]"""
        # 시뮬레이션된 LDAP 필터 생성
        ldap_filter = f"(uid={username})"
        
        # 위험한 문자들이 있는지 확인하지 않음
        dangerous_chars = ['*', '(', ')', '\\', '/', '\x00']
        found_dangerous = [char for char in dangerous_chars if char in username]
        
        return f"LDAP Filter: {ldap_filter}\nDangerous chars found: {found_dangerous}\n" + \
               f"This could be exploited with input like: *))(uid=*"

    # ===============================
    # 취약점 9: XML 외부 엔티티 (XXE) 시뮬레이션
    # ===============================
    @server.tool()
    def parse_xml_unsafe(xml_content: str) -> str:
        """XML을 파싱합니다. [취약점: XXE 공격 가능]"""
        import xml.etree.ElementTree as ET
        try:
            # 위험: 외부 엔티티 처리가 활성화됨
            root = ET.fromstring(xml_content)
            return f"Parsed XML root tag: {root.tag}, text: {root.text}"
        except Exception as e:
            return f"XML parsing error: {str(e)}"

    # ===============================
    # 원래 기능 (안전한 버전)
    # ===============================
    @server.tool()
    def count_character(text: str, character: str) -> int:
        """문자열에서 특정 문자의 개수를 셉니다. [안전한 기능]"""
        if len(character) != 1:
            raise ValueError("Character must be a single character")
        return text.count(character)

    # ===============================
    # 리소스: 보안 가이드라인
    # ===============================
    @server.resource("security://guidelines")
    def security_guidelines() -> str:
        """MCP 서버 보안 가이드라인"""
        return """
# MCP 서버 보안 가이드라인

## 1. 입력 검증
- 모든 사용자 입력을 검증하고 새니타이즈
- 화이트리스트 기반 검증 사용
- 길이 제한 및 타입 검증

## 2. 명령어 실행 방지
- subprocess.run()에서 shell=True 사용 금지
- 사용자 입력을 직접 시스템 명령어에 전달 금지
- 필요시 paramiko, fabric 등 안전한 라이브러리 사용

## 3. 파일 시스템 접근 제한
- 경로 순회 공격 방지를 위한 경로 검증
- chroot jail 또는 샌드박스 환경 사용
- 절대 경로 사용 및 상대 경로 제한

## 4. 직렬화 보안
- pickle 대신 JSON 사용
- 신뢰할 수 없는 데이터의 역직렬화 금지
- 스키마 검증 구현

## 5. 데이터베이스 보안
- 매개변수화된 쿼리 사용
- ORM 사용 권장
- 최소 권한 원칙 적용

## 6. 정보 노출 방지
- 오류 메시지에서 시스템 정보 노출 방지
- 로그에 민감한 정보 기록 금지
- 환경 변수 노출 방지

## 7. 리소스 제한
- 메모리 사용량 제한
- 실행 시간 제한
- 파일 크기 제한

## 8. 인증 및 권한
- 강력한 인증 메커니즘 구현
- 세션 관리 보안
- 최소 권한 원칙
"""

    @server.prompt()
    def security_audit_prompt(tool_name: str) -> list:
        """특정 도구의 보안 감사를 위한 프롬프트"""
        return [
            {
                "role": "user",
                "content": f"다음 MCP 도구의 보안 취약점을 분석해주세요: {tool_name}. "
                          f"취약점의 종류, 공격 시나리오, 그리고 해결 방안을 제시해주세요."
            }
        ]

    return server