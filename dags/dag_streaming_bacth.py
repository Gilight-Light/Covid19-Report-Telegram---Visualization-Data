from airflow.decorators import dag
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime, timedelta
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

@dag(
    dag_id='streaming_api_to_postgres',
    default_args=default_args,
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=['streaming', 'api', 'pyspark'],
)
def streaming_dag():
    # SparkSubmitOperator để chạy Spark Streaming script
    stream_task = SparkSubmitOperator(
        task_id='run_spark_streaming',
        application='./include/script/streamingpostgres.py',  
        conn_id='spark_default',
        name='streaming_api_to_postgres',
        driver_memory='1g',
        executor_memory='1g',
        executor_cores=1,
        num_executors=2,
    )

    stream_task

# Instantiate DAG
dag = streaming_dag()
