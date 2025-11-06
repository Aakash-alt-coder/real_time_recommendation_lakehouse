"""
Airflow DAG for ETL orchestration
"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from jobs.batch.ingest_user_profile import main as ingest_user_profile
from jobs.batch.ingest_product_catalog import main as ingest_product_catalog

default_args = {
    'owner': 'data_eng',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('etl_lakehouse', default_args=default_args, schedule_interval='@daily')

task_user_profile = PythonOperator(
    task_id='ingest_user_profile',
    python_callable=ingest_user_profile,
    dag=dag
)

task_product_catalog = PythonOperator(
    task_id='ingest_product_catalog',
    python_callable=ingest_product_catalog,
    dag=dag
)

task_user_profile >> task_product_catalog
