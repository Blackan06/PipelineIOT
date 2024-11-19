#!/bin/bash

# Kiểm tra kết nối PostgreSQL
echo "Đang chờ PostgreSQL sẵn sàng..."
while ! nc -z postgres 5432; do
  sleep 1
  echo "Đợi PostgreSQL sẵn sàng..."
done
echo "PostgreSQL đã sẵn sàng."

# Khởi tạo cơ sở dữ liệu cho Airflow (nếu cần thiết)
echo "Khởi tạo database cho Airflow..."
airflow db migrate

# Khởi động Airflow webserver
echo "Khởi động Airflow webserver..."
airflow webserver -p 8080 &

# Khởi động Airflow scheduler
echo "Khởi động Airflow scheduler..."
airflow scheduler &

# Đảm bảo rằng các quá trình tiếp tục chạy
wait
