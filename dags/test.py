from airflow.decorators import dag, task
from datetime import datetime
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyDatasetOperator
from google.cloud import bigquery
import pandas as pd

@task
def transfer_data_to_bigquery():
    # Khởi tạo hooks
    pg_hook = PostgresHook(postgres_conn_id='postgres_connect_Project')
    bq_hook = BigQueryHook(gcp_conn_id='gcp')

    # Truy vấn PostgreSQL với tên cột chính xác
    sql_query = """
        SELECT 
            province_state,
            country_region,
            lat,
            long,
            date,
            confirmed,
            deaths,
            recovered,
            active,
            who_region
        FROM covid19
    """
    df = pg_hook.get_pandas_df(sql_query)
    
    print("Columns in DataFrame:", df.columns.tolist())

    # Cấu hình BigQuery
    project_id = 'learn-dbt-439206'
    dataset_id = 'retail_test'
    table_id = 'covid19'
    
    # Chuyển đổi kiểu dữ liệu
    df['date'] = pd.to_datetime(df['date'].str.split().str[0], format='%Y-%m-%d')
    df['lat'] = df['lat'].astype(float)
    df['long'] = df['long'].astype(float)
    df['confirmed'] = df['confirmed'].astype(int)
    df['deaths'] = df['deaths'].astype(int)
    df['recovered'] = df['recovered'].astype(int)
    df['active'] = df['active'].astype(int)
    
    # Get BigQuery client
    client = bq_hook.get_client()
    table_ref = f"{project_id}.{dataset_id}.{table_id}"

    # Schema khớp với tên cột PostgreSQL
    schema = [
        bigquery.SchemaField("province_state", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("country_region", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("lat", "FLOAT64", mode="REQUIRED"),
        bigquery.SchemaField("long", "FLOAT64", mode="REQUIRED"),
        bigquery.SchemaField("date", "DATE", mode="REQUIRED"),
        bigquery.SchemaField("confirmed", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("deaths", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("recovered", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("active", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("who_region", "STRING", mode="REQUIRED")
    ]

    # Cấu hình job
    job_config = bigquery.LoadJobConfig(
        schema=schema,
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
    )

    # Load data vào BigQuery
    job = client.load_table_from_dataframe(
        df,
        table_ref,
        job_config=job_config
    )
    
    # Đợi job hoàn thành
    job.result()
    
    print(f"Đã tải {len(df)} dòng vào {table_ref}")
    return "Chuyển dữ liệu thành công"

@dag(
    dag_id='retail_covid_etl',
    start_date=datetime(2023, 1, 1),
    schedule=None,
    catchup=False,
    tags=['retail-test'],
)
def retail():
    # Tạo dataset
    create_dataset = BigQueryCreateEmptyDatasetOperator(
        task_id='create_retail_dataset',
        dataset_id='retail_test',
        gcp_conn_id='gcp',
    )

    # Task chuyển dữ liệu
    transfer_task = transfer_data_to_bigquery()

    # Định nghĩa thứ tự
    create_dataset >> transfer_task

# Khởi tạo DAG
dag = retail()