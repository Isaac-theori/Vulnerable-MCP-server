# 🚨 취약한 MCP 서버 - 보안 교육용 데모

⚠️ **경고: 이 서버는 교육 목적으로만 설계되었으며, 실제 운영 환경에서는 절대 사용하지 마세요!**

## 개요

이 프로젝트는 MCP (Model Context Protocol) 서버의 일반적인 보안 취약점들을 시연하고, 안전한 개발 방법을 교육하기 위해 설계되었습니다.

## 포함된 취약점들

1. **명령어 주입 (Command Injection)** - `execute_system_command`
2. **경로 순회 공격 (Path Traversal)** - `read_file_content`, `write_file_content`
3. **비직렬화 공격 (Deserialization)** - `process_pickled_data`
4. **SQL 인젝션** - `search_user_database`
5. **민감한 정보 노출** - `get_system_info`
6. **서비스 거부 공격 (DoS)** - `generate_large_data`
7. **임시 파일 보안** - `create_temp_file`
8. **LDAP 인젝션** - `ldap_search_simulation`
9. **XML 외부 엔티티 (XXE)** - `parse_xml_unsafe`

## 설치 및 실행

### 1. 의존성 설치
```bash
# uv 사용 (권장)
uv sync

# 또는 pip 사용
pip install -e .
```

### 2. 서버 실행
```bash
# 개발 모드로 실행
uv run dev

# 또는 실행 스크립트 사용
python run_server.py
```

### 3. 대화형 테스트
```bash
# 대화형 플레이그라운드
uv run playground
```

## 취약점 테스트

취약점을 안전하게 테스트해보려면:

```bash
# 취약점 테스트 스크립트 실행
python test_vulnerabilities.py
```

## 교육 자료

- [`SECURITY_DEMO.md`](SECURITY_DEMO.md) - 상세한 취약점 설명과 공격 시나리오
- [`test_vulnerabilities.py`](test_vulnerabilities.py) - 취약점 테스트 스크립트
- [`src/character_counter/server.py`](src/character_counter/server.py) - 취약한 서버 구현

## 학습 목표

이 프로젝트를 통해 다음을 학습할 수 있습니다:

1. 일반적인 웹 애플리케이션 취약점들이 MCP 서버에서 어떻게 나타나는지
2. 각 취약점의 공격 벡터와 영향도
3. 안전한 코딩 방법과 방어 기법
4. 보안 테스트 및 감사 방법

## 실습 과제

1. **취약점 분석**: 각 도구의 취약점을 식별하고 공격 시나리오를 작성하세요
2. **안전한 구현**: 취약한 기능들의 안전한 버전을 구현해보세요
3. **보안 테스트**: 구현한 안전한 버전을 테스트해보세요
4. **가이드라인 작성**: 조직의 MCP 서버 보안 가이드라인을 작성해보세요

## 보안 원칙

MCP 서버 개발 시 다음 원칙을 따르세요:

1. **최소 권한 원칙**: 필요한 최소한의 권한만 부여
2. **입력 검증**: 모든 사용자 입력을 검증하고 새니타이즈
3. **샌드박스 사용**: 격리된 환경에서 실행
4. **정기적인 보안 감사**: 코드와 설정을 정기적으로 검토
5. **보안 업데이트**: 의존성을 최신 상태로 유지

## 경고 및 면책 조항

⚠️ **이 프로젝트는 오직 교육 목적으로만 설계되었습니다.**

- 실제 운영 환경에서는 절대 사용하지 마세요
- 무단으로 타인의 시스템에 대해 테스트하지 마세요
- 취약점을 악용하여 불법적인 행위를 하지 마세요
- 사용자는 이 코드의 사용에 대한 모든 책임을 집니다

## 라이센스

이 프로젝트는 교육 목적으로만 제공됩니다. 상업적 사용을 금지합니다.
