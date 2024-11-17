# Sử dụng Python base image phù hợp
FROM python:3.9-slim

WORKDIR /app

# Cài đặt các thư viện cần thiết
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
# Thêm mã nguồn Producer vào container
COPY kafka_producer.py /app/kafka_producer.py

# Thiết lập entrypoint để khởi chạy Producer
CMD ["python", "kafka_producer.py"]
