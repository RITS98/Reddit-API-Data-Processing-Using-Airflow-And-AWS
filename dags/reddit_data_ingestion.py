from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
import sys

# Add the airflow directory to Python path to access pipelines and utils
sys.path.insert(0, '/opt/airflow')

from pipelines.reddit_pipeline import extract_reddit_data
from utils.constants import INPUT_PATH, OUTPUT_PATH
from pipelines.aws_s3_pipeline import upload_s3_pipeline



default_args ={
    'owner': "Ritayan Patra",
    'start_date': datetime(2025, 7, 13)
}

dynamic_file_name = datetime.now().strftime('%Y%m%d_%H%M%S')

with DAG(
    dag_id='reddit_data_ingestion',
    default_args=default_args,
    schedule='@daily',
    catchup=False,                      # Used for backfilling
    tags=['reddit', 'etl', 'pipeline']
) as dag:
    
    extract = PythonOperator(
        task_id = 'extract_reddit_data',
        python_callable=extract_reddit_data,
        op_kwargs={
            'file_name': f'reddit_{dynamic_file_name}',
            'subreddit': 'dataengineering',
            'time_filter': 'day',
            'limit': 1000
        }
    )

    upload_to_s3 = PythonOperator(
        task_id='upload_to_s3',
        python_callable=upload_s3_pipeline
    )

    extract >> upload_to_s3

    
    
