import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
from supabase import create_client


supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_KEY')

client = create_client(supabase_url, supabase_key)

# create a function for getting the traffic volume data from Open Toronto
def fetch_and_push_traffic_data():
    base_url = "https://ckan0.cf.opendata.inter.prod-toronto.ca"
    url = base_url + "/api/3/action/package_show"    
    params = { "id": "traffic-volumes-at-intersections-for-all-modes"}
    package = requests.get(url, params=params).json()

    for resource in package["result"]["resources"]:
        if resource["datastore_active"]:
            url = base_url + "/datastore/dump/" + resource["id"]
            resource_dump_data = requests.get(url).json()
            process_and_push_data(resource_dump_data)

# function to upsert the data to supabase
def process_and_push_data(data):
    table_name = 'traffic_data'

    response = client.table(table_name).upsert(data)
    if response['status'] == 201:
        print(f"Data successfully pushed to {table_name} in Supabase")
    else:
        print(f"Error pushing data to {table_name} in Supabase: {response}")

# DAG definition
dag = DAG(
    dag_id='toronto_traffic_data_pipeline',
    tags=['toronto'],
    description='A DAG to fetch traffic data from Toronto Open Data and push it to Supabase',
    schedule_interval='@daily',
    start_date=datetime(2024, 2, 13),
    catchup=False
)

fetch_and_push_traffic_data_task = PythonOperator(
    task_id='fetch_and_push_traffic_data_task',
    python_callable=fetch_and_push_traffic_data,
    dag=dag
)

# Define the task dependencies
fetch_and_push_traffic_data_task
