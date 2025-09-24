#!/bin/bash
cd /app

# 환경 변수 설정
export PYTHONPATH="/app/src:$PYTHONPATH"

# 여러 방법으로 서버 실행 시도
echo "🚨 교육용 취약점 MCP 서버 시작 중..."

# 방법 1: 직접 실행 스크립트
if [ -f "run_server.py" ]; then
    echo "run_server.py로 실행 중..."
    python run_server.py
elif command -v smithery &> /dev/null; then
    echo "smithery CLI로 실행 중..."
    smithery dev
else
    echo "Python 모듈로 실행 중..."
    python -m smithery.cli.dev
fi 