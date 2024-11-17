from datetime import datetime, timedelta
from airflow.decorators import dag, task
from airflow.providers.docker.operators.docker import DockerOperator
from include.iot_streaming.task import _produce_message
from airflow.operators.python import PythonOperator
from include.iot_streaming.task import process_batch_from_db
from airflow.models.baseoperator import chain

# Định nghĩa các default arguments cho DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    
}

# Định nghĩa DAG với decorator
@dag(
    default_args=default_args,
    description='DAG for IoT Data Pipeline using Kafka and Spark',
    schedule_interval=None,
    start_date=datetime(2024, 11, 11),
    catchup=False,
    tags=['iot_pipeline_dag'],
)
def iot_pipeline_dag():

    produce_message = DockerOperator(
        task_id='produce_message',
        image='airflow/kafka_producer',  
        api_version='auto',
        auto_remove=True,
        container_name='run_kafka_producer',
        docker_url='tcp://docker-proxy:2375',
        network_mode='container:kafka',
    )

    consume_message = DockerOperator(
        task_id='consume_message',
        image='airflow/kafka_consumer',  
        api_version='auto',
        auto_remove=True,
        container_name='run_kafka_consumer',
        docker_url="tcp://docker-proxy:2375",
        network_mode='container:kafka',
    )
    run_spark_job = DockerOperator(
        task_id='run_spark_job',
        image='airflow/iot_stream_analysis',
        api_version='auto',
        auto_remove=True,
        tty=True,
        xcom_all=False,
        mount_tmp_dir=False,
        container_name='run_spark_job_container',
        docker_url='tcp://docker-proxy:2375',
        network_mode='container:spark-master',
        environment={
            'SPARK_APPLICATION_ARGS': '{{ ti.xcom_pull(task_ids="consume_data_from_kafka")}}',
            'SHARED_VOLUME_PATH': '/shared_volume'
        },
        do_xcom_push=True,
    )
    def save_to_postgres_task():
        process_batch_from_db()

    save_to_postgres = PythonOperator(
        task_id='save_to_postgres',
        python_callable=save_to_postgres_task,
        provide_context=True,
    )
    chain(produce_message , [consume_message, run_spark_job], save_to_postgres)

iot_pipeline_dag()