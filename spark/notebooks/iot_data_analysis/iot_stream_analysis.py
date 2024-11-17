from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, StringType, FloatType
import psycopg2
from psycopg2 import sql
from datetime import datetime
from psycopg2.extras import execute_batch

# Tạo SparkSession với cấu hình để tải Kafka dependencies
spark = SparkSession.builder \
    .appName("IoT Stream Analysis") \
    .master("spark://spark-master:7077") \
    .getOrCreate()


# Định nghĩa schema cho dữ liệu JSON
schema = StructType([
    StructField("device_id", StringType(), True),
    StructField("temperature", FloatType(), True)
])

# Đọc dữ liệu từ Kafka topic "iot_data"
kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "iot_data") \
    .option("startingOffsets", "earliest") \
    .load()

iot_df = kafka_df.selectExpr("CAST(key AS STRING) as device_id", "CAST(value AS STRING) as value")

processed_df = iot_df.withColumn("jsonData", from_json(col("value"), schema)) \
    .select("device_id", "jsonData.*")  

def write_to_postgres(batch_df, batch_id):
    try:
        pandas_df = batch_df.toPandas()

        # Kết nối PostgreSQL
        connection = psycopg2.connect(
            database="iot_database",
            user="postgres",
            password="postgres",
            host="postgres",
            port="5432"
        )
        cursor = connection.cursor()
        cursor.execute("SELECT to_regclass('public.iot_data')")
        result = cursor.fetchone()

        if result[0] is not None:
            print("Bảng 'iot_data' tồn tại.")
        else:
            print("Bảng 'iot_data' không tồn tại.")
            
        cursor.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'iot_data' AND table_schema = 'public'
        """)
        columns = cursor.fetchall()

        # In ra các cột
        print("Columns in 'iot_data' table:")
        for column in columns:
            print(column[0])
        
        cursor.execute("INSERT INTO iot_data (device_id, temperature) VALUES (%s, %s)",("device_1", 12))
        cursor.execute("SELECT * FROM iot_data;")
        cursor.fetchone()
        # Commit dữ liệu
        connection.commit()
        cursor.close()
        connection.close()
        print(f"Batch {batch_id} inserted into PostgreSQL")
    except Exception as e:
        print(f"Error while inserting batch {batch_id}: {e}")
        
        
query = processed_df.writeStream \
    .foreachBatch(write_to_postgres) \
    .outputMode("append") \
    .start()

try:
    query.awaitTermination(timeout=60)  
    if not query.isActive:
        print("Query has stopped. No more data available, marking task as success.")
except Exception as e:
    print(f"Streaming query terminated with error: {e}")
    query.stop()

