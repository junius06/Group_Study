# 베이스 이미지로 Python 3.12.3 사용
FROM python:3.12.3

RUN apt -y update && apt -y install ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정
WORKDIR /app

# 필요 패키지 설치를 위한 requirements.txt 복사
COPY requirements.txt requirements.txt

# 필요 패키지 설치
RUN pip install -r requirements.txt

# 실행코드와 env파일 복사
COPY bot.py bot.py
COPY .env/ .env/

# 컨테이너에서 Streamlit 애플리케이션 실행
CMD ["streamlit", "run", "bot.py"]

# 포트 설정
EXPOSE 8501