from airflow.decorators import dag, task
from datetime import datetime
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook
import pandas as pd
from __future__ import annotations

import os
from datetime import datetime

from airflow.models.dag import DAG
from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryCreateEmptyDatasetOperator,
    BigQueryDeleteDatasetOperator,
    BigQueryGetDatasetOperator,
    BigQueryUpdateDatasetOperator,
)
from airflow.providers.standard.operators.bash import BashOperator
from airflow.utils.trigger_rule import TriggerRule

PROJECT_ID = "learn-dbt-439206"
DATASET_ID = "retail"
TABLE_ID = "covid19"

@dag(
    start_date=datetime(2023, 1, 1),
    schedule=None,
    catchup=False,
    tags=['retail'],
)
def retail():
    
    @task()
    def check_and_create_dataset():
        # Sử dụng BigQueryHook từ Airflow với kết nối đã cấu hình
        bigquery_hook = BigQueryHook(gcp_conn_id='gcp')
        dataset_ref = bigquery_hook.get_dataset_ref(PROJECT_ID, DATASET_ID)
        try:
            bigquery_hook.get_conn().get_dataset(dataset_ref)  # Kiểm tra nếu dataset đã tồn tại
            return f"Dataset '{DATASET_ID}' đã tồn tại."
        except Exception as e:
            # Nếu không tồn tại, tạo mới dataset
            bigquery_hook.create_empty_dataset(PROJECT_ID, DATASET_ID)
            return f"Dataset '{DATASET_ID}' đã được tạo."

    @task()
    def extract_data_from_postgres():
        hook = PostgresHook(postgres_conn_id='postgres_connect_Project')
        sql_query = "SELECT * FROM public.covid19"
        connection = hook.get_conn()
        cursor = connection.cursor()
        cursor.execute(sql_query)
        data = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(data, columns=columns)
        cursor.close()
        connection.close()
        return df

    @task()
    def load_data_to_bigquery(df):
        # Sử dụng BigQueryHook từ Airflow với kết nối đã cấu hình
        bigquery_hook = BigQueryHook(gcp_conn_id='gcp')
        
        table_id = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"
        
        # Load dữ liệu từ DataFrame lên BigQuery
        job_config = {
            "writeDisposition": "WRITE_TRUNCATE",  # Thay đổi chế độ theo nhu cầu (WRITE_APPEND nếu cần thêm dữ liệu)
            "autodetect": True,  # Tự động phát hiện schema
        }
        
        # Upload DataFrame vào BigQuery
        bigquery_hook.insert_rows_from_dataframe(df, table_id, row_ids=None, **job_config)

        return f"Dữ liệu đã được load vào bảng {TABLE_ID} trong dataset {DATASET_ID}."

    # Task dependencies
    dataset_status = check_and_create_dataset()
    df = extract_data_from_postgres()
    load_data_to_bigquery(df)

retail()
