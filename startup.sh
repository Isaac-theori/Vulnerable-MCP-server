#!/bin/bash
cd /app

# 환경 변수 설정
export PYTHONPATH="/app/src:$PYTHONPATH"

echo "🚨 교육용 취약점 MCP 서버 시작 중..."
echo "⚠️ 이 서버는 교육용으로만 사용하세요!"

# Python 3가 있는지 확인하고 사용
if command -v python3 &> /dev/null; then
    echo "Python3으로 실행 중..."
    python3 -m smithery.cli.dev
elif command -v python &> /dev/null; then
    echo "Python으로 실행 중..."
    python -m smithery.cli.dev
else
    echo "오류: Python을 찾을 수 없습니다!"
    exit 1
fi 