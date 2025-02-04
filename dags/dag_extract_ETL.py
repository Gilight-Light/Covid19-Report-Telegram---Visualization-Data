from airflow import DAG
from airflow.decorators import dag, task
from airflow.providers.postgres.operators.postgres import PostgresOperator
from pyspark.sql import SparkSession
from pyspark.sql.functions import expr
from datetime import datetime, timedelta


dag_owner = 'airflow'

default_args = {
    'owner': dag_owner,
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=3),
}

@dag(
    dag_id='SQL_Postgres_ETL',
    default_args=default_args,
    description='Extract And ETL into Postgres DB',
    start_date=datetime(2024, 11, 7),
    schedule_interval=None,
    catchup=False,
    tags=['']
)
def etl_dag():
    # Task 1: Create table in Postgres
    create_table = PostgresOperator(
        task_id='create_table',
        postgres_conn_id='postgres_connect_Project',
        sql='sql/create_table.sql',
    )

    # Task 2: Read and process data using PySpark
    @task()
    def read_data():
        spark = SparkSession.builder \
            .config("spark.jars.packages", "org.postgresql:postgresql:42.2.5") \
            .appName("Covid19 Data Processing") \
            .getOrCreate()

        data_path = "./include/dataset/covid_19_clean_complete.csv"
        
        # Read CSV
        df = spark.read.csv(data_path, header=True, inferSchema=True)

        # Rename columns
        df = df.withColumnRenamed("Province/State", "province_state") \
                .withColumnRenamed("Country/Region", "country_region") \
                .withColumnRenamed("Lat", "lat") \
                .withColumnRenamed("Long", "long") \
                .withColumnRenamed("Date", "date") \
                .withColumnRenamed("Confirmed", "confirmed") \
                .withColumnRenamed("Deaths", "deaths") \
                .withColumnRenamed("Recovered", "recovered") \
                .withColumnRenamed("Active", "active") \
                .withColumnRenamed("WHO Region", "who_region")
        

        # Write to PostgreSQL
        df.write \
            .format('jdbc') \
            .option('url', 'jdbc:postgresql://host.docker.internal:5436/postgres') \
            .option('dbtable', 'public.covid19') \
            .option('user', 'postgres') \
            .option('password', 'postgres') \
            .option('driver', 'org.postgresql.Driver') \
            .mode('append') \
            .save()

        spark.stop()

    # Define task dependencies using TaskFlow API
    create_table >> read_data()

# Instantiate the DAG
etl_dag()
