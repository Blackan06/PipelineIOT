FROM  bitnami/spark:latest


# Switch to root user to install dependencies
USER root

# Update the apt repository and install necessary packages
RUN apt-get update && \
    apt-get install -y wget curl && \
    apt-get clean

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

RUN wget https://jdbc.postgresql.org/download/postgresql-42.6.0.jar \
    && mv postgresql-42.6.0.jar /opt/bitnami/spark/jars/
# Set Spark environment variables
ENV SPARK_HOME=/opt/bitnami/spark
ENV PATH=$SPARK_HOME/bin:$PATH
ENV SPARK_JARS_DIR=$SPARK_HOME/jars


# Set up the working directory and copy the requirements.txt file
WORKDIR /app
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . /app


CMD ["spark-submit", "--master", "spark://spark-master:7077", "iot_stream_analysis.py"]
