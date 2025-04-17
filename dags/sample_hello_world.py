# simple_hello_world_01.py


from datetime import datetime, timedelta
from airflow.utils.dates import days_ago

# initiate DAG
from airflow import DAG

# this is first task
from airflow.operators.bash import BashOperator

default_args = {
    'owner' : 'tasneemahmed',
}

with DAG(
    dag_id='hello_world',
    description = 'Our first "Hello World" DAG!',
    default_args = default_args,
    start_date = days_ago(1),
    schedule_interval = '@daily',
    tags = ['beginner', 'bach', 'hello_world']
) as dag:

    # this is the first task, by with keyword and this way we can avoid using the 'dag' parameter
    task = BashOperator(
        task_id = 'hello_world_task',
        bash_command = 'echo Hello world once again!'
    )

task

