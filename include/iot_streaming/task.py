from airflow.hooks.base import BaseHook
from airflow.exceptions import AirflowNotFoundException
import requests
import json
from io import BytesIO
from confluent_kafka import Producer
import psycopg2
from psycopg2 import sql
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine

def _produce_message():
    conf = {
        'bootstrap.servers': 'kafka:9092',  
        'client.id': 'airflow-producer'
    }
    producer = Producer(conf)
    producer.produce('iot_data', key='device1', value='{"temperature": 25.5}')
    producer.flush()
    
def process_batch_from_db():
    # Kết nối DB
    connection = psycopg2.connect(
        database="iot_database",
        user="postgres",
        password="postgres",
        host="postgres",
        port="5432"
    )
    
    # Lấy batch dữ liệu chưa xử lý
    query = """
            SELECT * FROM iot_data
            WHERE processed = FALSE
            LIMIT 100
            """
    df = pd.read_sql(query, connection)
    
    print(df)
    # Xử lý batch
    for index, row in df.iterrows():
        print(f"Processing: {row['device_id']}, Temperature: {row['temperature']}")
        # Update trạng thái là đã xử lý
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE iot_data SET processed = TRUE WHERE id = %s",
            (row['id'],)
        )
        connection.commit()
    
    connection.close()