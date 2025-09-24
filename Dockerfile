FROM python:3.11-slim

WORKDIR /app

# 시스템 패키지 업데이트 및 필요한 패키지 설치
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 설치를 위한 파일들 복사
COPY pyproject.toml uv.lock ./

# uv 설치
RUN pip install uv

# 의존성 설치
RUN uv sync --no-dev

# 소스 코드 복사
COPY . .

# 실행 권한 부여
RUN chmod +x startup.sh

# 환경 변수 설정
ENV PYTHONPATH=/app/src
ENV PORT=8000

# 포트 노출
EXPOSE 8000

# 서버 시작
CMD ["./startup.sh"] 