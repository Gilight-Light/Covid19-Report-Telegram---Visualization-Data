import os 
from datetime import datetime, timedelta

from airflow.models.DAG import DAG, TaskInstance
from airflow.providers.google.cloud.operators.bigquery import (
    BigqueryEmptyOperator,
    BigQueryCreateEmptyDatasetOperator,
    BigQueryCreateExternalTableOperator,
    BigQueryCreateTableOperator,
)
from airflow.providers.google.cloud.transfers.postgres_to_bigquery import PostgresToBigQueryOperator

from airflow.ultis.trigger.rule import TriggerRule

DAG_ID = "google_bigquery"

