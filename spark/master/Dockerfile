# Dockerfile cho Spark Master sử dụng base image đã có Spark, Scala, và Java
FROM  bitnami/spark:latest

LABEL maintainer="Anh Kiet <huynhanhkiet2222@gmail.com>"

USER root
RUN apt-get update && apt-get install -y wget
# Cài đặt thêm các gói cần thiết
COPY master.sh /

RUN wget https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.5.3/spark-sql-kafka-0-10_2.12-3.5.3.jar \
    && wget https://repo1.maven.org/maven2/org/apache/spark/spark-streaming-kafka-0-10_2.12/3.5.3/spark-streaming-kafka-0-10_2.12-3.5.3.jar \
    && wget https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_2.12/3.5.3/spark-token-provider-kafka-0-10_2.12-3.5.3.jar \
    && wget https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.4.1/kafka-clients-3.4.1.jar \
    && wget https://repo1.maven.org/maven2/org/apache/commons/commons-pool2/2.11.0/commons-pool2-2.11.0.jar \
    && mv spark-sql-kafka-0-10_2.12-3.5.3.jar /opt/bitnami/spark/jars/ \
    && mv spark-streaming-kafka-0-10_2.12-3.5.3.jar /opt/bitnami/spark/jars/ \
    && mv spark-token-provider-kafka-0-10_2.12-3.5.3.jar /opt/bitnami/spark/jars/ \
    && mv kafka-clients-3.4.1.jar /opt/bitnami/spark/jars/ \
    && mv commons-pool2-2.11.0.jar /opt/bitnami/spark/jars/

ENV SPARK_MASTER_PORT 7077
ENV SPARK_MASTER_WEBUI_PORT 8080
ENV SPARK_MASTER_LOG /opt/bitnami/spark/logs

EXPOSE 8080 7077 6066

CMD ["/bin/bash", "/master.sh"]