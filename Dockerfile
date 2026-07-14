FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y wget unzip && \
    wget -q https://github.com/SagerNet/sing-box/releases/latest/download/sing-box-linux-amd64.zip && \
    unzip sing-box-linux-amd64.zip && \
    mv sing-box /usr/local/bin/ && \
    chmod +x /usr/local/bin/sing-box && \
    rm sing-box-linux-amd64.zip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
