#!/bin/bash
set -e

echo "🚨 교육용 취약점 MCP 서버 시작 중..."
echo "⚠️ 이 서버는 교육용으로만 사용하세요!"

# 환경 변수 설정
export PYTHONPATH="/app/src:/app:$PYTHONPATH"

cd /app

# 가상환경이 있으면 활성화
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Smithery dev 실행
exec python -m smithery.cli.dev 