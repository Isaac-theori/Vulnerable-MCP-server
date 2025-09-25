# MCP 서버 보안 취약점 교육 데모

⚠️ **경고: 이 서버는 교육 목적으로만 설계되었으며, 실제 운영 환경에서는 절대 사용하지 마세요!**

## 개요

이 프로젝트는 MCP (Model Context Protocol) 서버의 일반적인 보안 취약점들을 시연하고, 안전한 개발 방법을 교육하기 위해 설계되었습니다.

## 포함된 취약점들

### 1. 명령어 주입 (Command Injection)
**도구명**: `execute_system_command`

**취약점**: 사용자 입력을 직접 시스템 셸에 전달
```python
# 위험한 예제
subprocess.run(command, shell=True, capture_output=True, text=True)
```

**공격 시나리오**:
```
입력: "ls; cat /etc/passwd"
결과: 디렉토리 목록 출력 후 시스템 사용자 정보 노출
```

**안전한 대안**:
```python
# 화이트리스트 기반 명령어 허용
allowed_commands = ['ls', 'pwd', 'date']
if command not in allowed_commands:
    raise ValueError("Command not allowed")
subprocess.run([command], capture_output=True, text=True)
```

### 2. 경로 순회 공격 (Path Traversal)
**도구명**: `read_file_content`, `write_file_content`

**취약점**: 파일 경로 검증 없이 파일 시스템 접근

**공격 시나리오**:
```
입력: "../../../etc/passwd"
결과: 시스템 사용자 정보 노출

입력: "../../../home/user/.ssh/id_rsa"
결과: SSH 개인키 노출
```

**안전한 대안**:
```python
import os
from pathlib import Path

def safe_path_join(base_dir, user_path):
    # 기준 디렉토리 설정
    base = Path(base_dir).resolve()
    # 사용자 경로를 기준 디렉토리와 결합
    target = (base / user_path).resolve()
    # 경로가 기준 디렉토리 내에 있는지 확인
    if not str(target).startswith(str(base)):
        raise ValueError("Invalid path")
    return target
```

### 3. 비직렬화 공격 (Deserialization Attack)
**도구명**: `process_pickled_data`

**취약점**: 신뢰할 수 없는 pickle 데이터 역직렬화

**공격 시나리오**:
```python
# 악성 pickle 데이터 생성
import pickle
import base64
import os

class MaliciousPayload:
    def __reduce__(self):
        return (os.system, ('rm -rf /tmp/*',))

payload = base64.b64encode(pickle.dumps(MaliciousPayload())).decode()
# 이 payload를 process_pickled_data에 전달하면 시스템 명령어 실행
```

**안전한 대안**:
```python
import json
from pydantic import BaseModel

# JSON 사용
data = json.loads(user_input)

# 또는 스키마 검증과 함께
class SafeData(BaseModel):
    name: str
    value: int

validated_data = SafeData.parse_obj(json.loads(user_input))
```

### 4. SQL 인젝션
**도구명**: `search_user_database`

**취약점**: 사용자 입력을 직접 SQL 쿼리에 포함

**공격 시나리오**:
```sql
-- 일반 입력
입력: "admin"
쿼리: SELECT * FROM users WHERE username = 'admin'

-- 악성 입력
입력: "admin'; DROP TABLE users; --"
쿼리: SELECT * FROM users WHERE username = 'admin'; DROP TABLE users; --'
결과: 전체 users 테이블 삭제

-- 정보 탈취
입력: "' OR '1'='1"
쿼리: SELECT * FROM users WHERE username = '' OR '1'='1'
결과: 모든 사용자 정보 반환
```

**안전한 대안**:
```python
# 매개변수화된 쿼리 사용
cursor.execute("SELECT * FROM users WHERE username = ?", (username,))

# 또는 ORM 사용
user = User.objects.filter(username=username).first()
```

### 5. 민감한 정보 노출
**도구명**: `get_system_info`

**취약점**: 시스템 환경 변수 및 내부 정보 노출

**위험성**:
- API 키, 비밀번호 등이 환경 변수에 저장된 경우 노출
- 시스템 구조 정보 노출로 추가 공격 벡터 제공

**안전한 대안**:
```python
# 필요한 정보만 선별적으로 노출
safe_info = {
    "server_version": "1.0.0",
    "python_version": platform.python_version(),
    "uptime": get_uptime()
}
```

### 6. 서비스 거부 공격 (DoS)
**도구명**: `generate_large_data`

**취약점**: 리소스 사용량 제한 없음

**공격 시나리오**:
```
입력: size_mb=10000 (10GB)
결과: 메모리 고갈로 서버 다운
```

**안전한 대안**:
```python
def generate_large_data(size_mb: int) -> str:
    MAX_SIZE_MB = 100  # 최대 100MB로 제한
    if size_mb > MAX_SIZE_MB:
        raise ValueError(f"Size cannot exceed {MAX_SIZE_MB}MB")
    
    # 메모리 효율적인 방법으로 생성
    return f"Would generate {size_mb}MB of data"
```

### 7. 임시 파일 보안
**도구명**: `create_temp_file`

**취약점**: 예측 가능한 임시 파일명

**위험성**:
- 경쟁 상태 (Race Condition) 공격
- 심볼릭 링크 공격

**안전한 대안**:
```python
import tempfile

def create_temp_file(content: str) -> str:
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write(content)
        return f.name
```

### 8. LDAP 인젝션
**도구명**: `ldap_search_simulation`

**취약점**: LDAP 필터에 사용자 입력 직접 포함

**공격 시나리오**:
```
입력: "*))(uid=*"
필터: (uid=*))(uid=*)
결과: 모든 사용자 정보 반환
```

### 9. XML 외부 엔티티 (XXE)
**도구명**: `parse_xml_unsafe`

**취약점**: 외부 엔티티 처리 활성화

**공격 시나리오**:
```xml
<?xml version="1.0"?>
<!DOCTYPE root [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<root>&xxe;</root>
```

**안전한 대안**:
```python
import xml.etree.ElementTree as ET

# 외부 엔티티 비활성화
ET.XMLParser(resolve_entities=False)
```

## 공격 시나리오 실습

### 시나리오 1: 시스템 침투
1. `get_system_info`로 시스템 정보 수집
2. `read_file_content`로 민감한 파일 접근 시도
3. `execute_system_command`로 추가 명령어 실행

### 시나리오 2: 데이터베이스 공격
1. `search_user_database`에서 SQL 인젝션으로 모든 사용자 정보 탈취
2. 관리자 계정 정보 확인
3. 시스템 권한 상승 시도

### 시나리오 3: 서비스 거부 공격
1. `generate_large_data`로 메모리 고갈 시도
2. 여러 요청을 동시에 보내 서버 다운

## 방어 전략

### 1. 입력 검증
```python
from pydantic import BaseModel, validator

class SafeInput(BaseModel):
    command: str
    
    @validator('command')
    def validate_command(cls, v):
        allowed = ['ls', 'pwd', 'date']
        if v not in allowed:
            raise ValueError('Command not allowed')
        return v
```

### 2. 샌드박스 환경
```python
import subprocess
import os

def run_in_sandbox(command):
    # Docker 컨테이너나 chroot jail 사용
    sandbox_cmd = f"docker run --rm alpine:latest {command}"
    return subprocess.run(sandbox_cmd.split(), capture_output=True)
```

### 3. 레이트 리미팅
```python
from functools import wraps
import time

def rate_limit(max_calls=10, period=60):
    def decorator(func):
        calls = {}
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            # 클라이언트 IP 기반 제한
            client_id = get_client_id()
            
            if client_id not in calls:
                calls[client_id] = []
            
            # 오래된 호출 제거
            calls[client_id] = [t for t in calls[client_id] if now - t < period]
            
            if len(calls[client_id]) >= max_calls:
                raise Exception("Rate limit exceeded")
            
            calls[client_id].append(now)
            return func(*args, **kwargs)
        
        return wrapper
    return decorator
```

### 4. 로깅 및 모니터링
```python
import logging

logger = logging.getLogger(__name__)

def secure_tool(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        client_info = get_client_info()
        logger.info(f"Tool {func.__name__} called by {client_info}")
        
        try:
            result = func(*args, **kwargs)
            logger.info(f"Tool {func.__name__} completed successfully")
            return result
        except Exception as e:
            logger.error(f"Tool {func.__name__} failed: {str(e)}")
            raise
    
    return wrapper
```

## 실습 과제

1. **취약점 식별**: 각 도구의 취약점을 식별하고 공격 방법을 설명하세요.
2. **안전한 버전 구현**: 취약한 도구들의 안전한 버전을 구현해보세요.
3. **보안 테스트**: 구현한 안전한 버전이 실제로 공격을 방어하는지 테스트해보세요.
4. **보안 가이드라인 작성**: 조직의 MCP 서버 개발 보안 가이드라인을 작성해보세요.

## 결론

MCP 서버는 강력한 기능을 제공하지만, 그만큼 보안에 대한 주의가 필요합니다. 항상 다음 원칙을 따르세요:

1. **최소 권한 원칙**: 필요한 최소한의 권한만 부여
2. **입력 검증**: 모든 사용자 입력을 검증
3. **샌드박스 사용**: 격리된 환경에서 실행
4. **정기적인 보안 감사**: 코드와 설정을 정기적으로 검토
5. **보안 업데이트**: 의존성을 최신 상태로 유지

이러한 원칙을 따라 안전하고 신뢰할 수 있는 MCP 서버를 개발하세요. 