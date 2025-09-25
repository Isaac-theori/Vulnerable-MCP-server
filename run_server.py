#!/usr/bin/env python3
"""
취약한 MCP 서버 실행 스크립트
⚠️ 교육 목적으로만 사용하세요!
"""

import subprocess
import sys
import os

def main():
    """서버 실행"""
    print("🚨 취약한 MCP 서버 시작 🚨")
    print("=" * 50)
    print("⚠️  경고: 이 서버는 의도적으로 취약합니다!")
    print("⚠️  교육 목적으로만 사용하세요!")
    print("⚠️  실제 운영 환경에서는 절대 사용하지 마세요!")
    print("=" * 50)
    
    # 현재 디렉토리가 올바른지 확인
    if not os.path.exists("src/character_counter/server.py"):
        print("❌ 오류: src/character_counter/server.py 파일을 찾을 수 없습니다.")
        print("올바른 디렉토리에서 실행하세요.")
        sys.exit(1)
    
    try:
        print("🚀 서버를 시작합니다...")
        print("🔗 서버가 시작되면 http://127.0.0.1:8082에서 접근 가능합니다.")
        print("🛑 서버를 중지하려면 Ctrl+C를 누르세요.")
        print()
        
        # uv run dev 실행
        subprocess.run(["uv", "run", "dev"], check=True)
        
    except KeyboardInterrupt:
        print("\n👋 서버가 중지되었습니다.")
    except subprocess.CalledProcessError as e:
        print(f"❌ 서버 실행 중 오류 발생: {e}")
        print("\n해결 방법:")
        print("1. uv가 설치되어 있는지 확인하세요")
        print("2. 'uv sync' 명령어로 의존성을 설치하세요")
        print("3. Python 3.11+ 버전이 설치되어 있는지 확인하세요")
    except Exception as e:
        print(f"❌ 예상치 못한 오류: {e}")

if __name__ == "__main__":
    main() 