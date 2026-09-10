FROM python:3.12-slim

WORKDIR /app

# نصب وابستگی‌های سیستم
RUN apt-get update && apt-get install -y \
    wget unzip curl \
    && rm -rf /var/lib/apt/lists/*

# دانلود و نصب Sing-box
RUN curl -L -o sing-box.tar.gz https://github.com/SagerNet/sing-box/releases/download/v1.12.0/sing-box-1.12.0-linux-amd64.tar.gz && \
    tar -xzf sing-box.tar.gz && \
    mv sing-box-1.12.0-linux-amd64/sing-box /usr/local/bin/ && \
    chmod +x /usr/local/bin/sing-box && \
    rm -rf sing-box.tar.gz sing-box-1.12.0-linux-amd64

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# پورت پیش‌فرض (Railway از $PORT استفاده می‌کنه)
ENV PORT=8000
EXPOSE 8000

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]