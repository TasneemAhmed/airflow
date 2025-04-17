
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago

# initiate DAG
from airflow import DAG

# this is first task
from airflow.operators.python import PythonOperator

import pandas as pd


default_args = {
    'owner' : 'tasneemahmed',
}

def read_csv_file():
    df = pd.read_csv('/home/tasneemahmed24/airflow/dataset/insurance.csv')
    print(df)
    return df.to_json()

# kwargs refer to recive number of arguments
def remove_null_values(**kwargs):
    df = pd.read_json(kwargs['ti'].xcom_pull(task_ids='read_csv_task'))
    filtered_df = df.dropna()
    print(filtered_df)
    return filtered_df.to_json()

def group_by_smoker(ti):
    df = pd.read_json(ti.xcom_pull(task_ids='remove_null_values_task'))
    grouped_df = df.groupby('smoker').agg(
        {'bmi': 'mean', 'age':'mean', 'charges': 'mean'}
        ).reset_index()
    print(grouped_df)
    grouped_df.to_csv('/home/tasneemahmed24/airflow/dataset/grouped_by_smoker.csv', index=False)
    return grouped_df.to_json()

def group_by_region(ti):
    df = pd.read_json(ti.xcom_pull(task_ids='remove_null_values_task'))
    # group by region and calculate mean of bmi, age and charges
    # and reset the index
    # this will create a new dataframe with the mean values of bmi, age and charges for each region
    # and the index will be reset to default integer index
    grouped_df = df.groupby('region').agg(
        {'bmi': 'mean', 'age':'mean', 'charges': 'mean'}
        ).reset_index()
    print(grouped_df)
    grouped_df.to_csv('/home/tasneemahmed24/airflow/dataset/grouped_by_region.csv', index=False)
    return grouped_df.to_json()

with DAG(
    dag_id='executing_Python_pipeline',
    description = 'Run Python pipeline',
    schedule_interval = '@once',
    tags = ['python scripts', 'pipeline'],    
    default_args = default_args,
    start_date = days_ago(1),
)as dag:
    # this is the first task, by with keyword and this way we can avoid using the 'dag' parameter
    read_csv = PythonOperator(
        task_id = 'read_csv_task',
        python_callable = read_csv_file,
    )
    # this is the second task
    remove_null_values = PythonOperator(
        task_id = 'remove_null_values_task',
        python_callable = remove_null_values,    
        )
    # this is the third task
    groube_by_smoker = PythonOperator(
        task_id = 'groube_by_smoker_task',
        python_callable = group_by_smoker,
    )
    # this is the fourth task
    groube_by_region = PythonOperator(
        task_id = 'groube_by_region_task',
        python_callable = group_by_region,
    )
read_csv >> remove_null_values >> [groube_by_smoker, groube_by_region]