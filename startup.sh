#!/bin/bash
set -e  # 오류 발생 시 스크립트 중단

cd /app

echo "🚨 교육용 취약점 MCP 서버 시작 중..."
echo "⚠️ 이 서버는 교육용으로만 사용하세요!"
echo "현재 디렉토리: $(pwd)"
echo "Python 경로 설정 중..."

# 환경 변수 설정
export PYTHONPATH="/app/src:/app:$PYTHONPATH"
export PATH="/app/.venv/bin:$PATH"

echo "설정된 PYTHONPATH: $PYTHONPATH"

# 가상환경 활성화 시도
if [ -f "/app/.venv/bin/activate" ]; then
    echo "가상환경 활성화 중..."
    source /app/.venv/bin/activate
fi

# 여러 방법으로 서버 실행 시도
echo "서버 실행 방법 탐색 중..."

# 방법 1: uv로 실행
if command -v uv &> /dev/null; then
    echo "uv로 실행 시도..."
    uv run python -m smithery.cli.dev
# 방법 2: Python3로 실행
elif command -v python3 &> /dev/null; then
    echo "Python3으로 실행 시도..."
    python3 -m smithery.cli.dev
# 방법 3: Python으로 실행
elif command -v python &> /dev/null; then
    echo "Python으로 실행 시도..."
    python -m smithery.cli.dev
# 방법 4: 직접 스크립트 실행
elif [ -f "run_server.py" ]; then
    echo "run_server.py로 실행 시도..."
    python3 run_server.py
else
    echo "❌ 오류: 서버를 실행할 방법을 찾을 수 없습니다!"
    echo "Python 버전: $(python3 --version 2>/dev/null || echo 'Python3 없음')"
    echo "uv 버전: $(uv --version 2>/dev/null || echo 'uv 없음')"
    exit 1
fi 