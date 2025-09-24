#!/usr/bin/env python3
"""
배포 환경에서 MCP 서버를 직접 실행하는 스크립트
"""

import sys
import os

# 현재 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from hello_server.server import create_server
    from mcp.server.fastmcp import FastMCP
    import uvicorn
    
    # 서버 생성
    server = create_server()
    
    # 서버 실행
    if __name__ == "__main__":
        # 환경 변수에서 포트 가져오기 (기본값: 8000)
        port = int(os.environ.get("PORT", 8000))
        host = os.environ.get("HOST", "0.0.0.0")
        
        print(f"🚨 교육용 취약점 서버 시작 중...")
        print(f"서버 주소: {host}:{port}")
        print("⚠️ 이 서버는 교육용으로만 사용하세요!")
        
        # FastMCP 서버를 uvicorn으로 실행
        uvicorn.run(
            server.app,
            host=host,
            port=port,
            log_level="info"
        )
        
except ImportError as e:
    print(f"모듈 import 오류: {e}")
    print("smithery.cli.dev를 사용합니다...")
    
    # fallback: smithery CLI 사용
    from smithery.cli.dev import main
    main()
except Exception as e:
    print(f"서버 실행 오류: {e}")
    sys.exit(1) 