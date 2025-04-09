import airflow
from airflow import DAG
from datetime import timedelta
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
import requests
import csv
from google.cloud import storage
import tempfile

default_args = {
    'start_date': airflow.utils.dates.days_ago(0),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'pipeline',
    default_args=default_args,
    description='Migration Project',
    schedule_interval='@daily',
    max_active_runs=2,
    catchup=False,
    dagrun_timeout=timedelta(minutes=10),
)

Dummy_task = DummyOperator(task_id='Dummy_task', dag=dag)

def fetch_and_upload():
    """Fetch API data, save it to a temporary CSV, and upload directly to GCS."""
    url = 'https://cricbuzz-cricket.p.rapidapi.com/stats/v1/rankings/batsmen'
    headers = {
        "x-rapidapi-key": "aa31a53a62msh513f1a022780c99p16c578jsn93c92a95573a",
        "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
    }
    params = {'formatType': 'odi'}
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json().get('rank', [])
        if not data:
            print("No data received from API.")
            return
        
        # Use a temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, newline='', encoding='utf-8') as temp_file:
            writer = csv.DictWriter(temp_file, fieldnames=['rank', 'name', 'country'])
            for entry in data:
                writer.writerow({field: entry.get(field) for field in ['rank', 'name', 'country']})
            
            temp_file_path = temp_file.name  # Get the file path
        
        # Upload to GCS
        client = storage.Client()
        bucket = client.get_bucket('ranking-data-1')
        blob = bucket.blob('batsmen_rankings.csv')
        blob.upload_from_filename(temp_file_path)
        print("File successfully uploaded to GCS.")
    
    else:
        print("API request failed:", response.status_code)

extract_and_upload_task = PythonOperator(
    task_id='fetch_and_upload',
    python_callable=fetch_and_upload,
    dag=dag
)

Dummy_task >> extract_and_upload_task
