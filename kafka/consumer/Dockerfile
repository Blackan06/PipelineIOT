# Sử dụng Python base image phù hợp
FROM python:3.9-slim

WORKDIR /app

# Cài đặt các thư viện cần thiết
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
# Thêm mã nguồn Consumer vào container
COPY kafka_consumer.py /app/kafka_consumer.py
# Thiết lập entrypoint để khởi chạy Consumer
CMD ["python", "kafka_consumer.py"]
