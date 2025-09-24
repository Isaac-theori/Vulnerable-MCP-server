#!/usr/bin/env python3
"""
배포 환경에서 MCP 서버를 직접 실행하는 스크립트
"""

import sys
import os

# 현재 디렉토리를 Python 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

def main():
    print("🚨 교육용 취약점 서버 시작 중...")
    print("⚠️ 이 서버는 교육용으로만 사용하세요!")
    
    try:
        # smithery dev 명령어 실행
        from smithery.cli.dev import main as smithery_main
        print("smithery dev로 서버 실행 중...")
        smithery_main()
        
    except Exception as e:
        print(f"서버 실행 오류: {e}")
        print("대체 방법을 시도 중...")
        
        # 대체 방법: 직접 모듈 실행
        try:
            import subprocess
            subprocess.run([sys.executable, "-m", "smithery.cli.dev"], 
                         cwd=current_dir, check=True)
        except Exception as e2:
            print(f"대체 방법도 실패: {e2}")
            sys.exit(1)

if __name__ == "__main__":
    main() 