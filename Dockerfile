FROM python:3.12-slim

WORKDIR /app

# نصب وابستگی‌های سیستم
RUN apt-get update && apt-get install -y \
    wget unzip curl \
    && rm -rf /var/lib/apt/lists/*

# دانلود و نصب Sing-box (نسخه‌ی پایدار)
RUN curl -L -o sing-box.zip https://github.com/SagerNet/sing-box/releases/download/v1.12.0/sing-box-1.12.0-linux-amd64.zip && \
    unzip sing-box.zip && \
    mv sing-box /usr/local/bin/ && \
    chmod +x /usr/local/bin/sing-box && \
    rm sing-box.zip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
