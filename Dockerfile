FROM quay.io/astronomer/astro-runtime:12.3.0

USER root

# Copy script khởi động vào container
COPY start_airflow.sh /start_airflow.sh

# Đảm bảo script có quyền thực thi
RUN chmod +x /start_airflow.sh

USER astro

# Thiết lập lệnh mặc định khi container chạy
ENTRYPOINT ["/start_airflow.sh"]