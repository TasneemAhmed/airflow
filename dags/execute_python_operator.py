

from datetime import datetime, timedelta
from airflow.utils.dates import days_ago

# initiate DAG
from airflow import DAG

# this is first task
from airflow.operators.python import PythonOperator

default_args = {
    'owner' : 'tasneemahmed',
}
# def task_a_func():  
#     print("Task A has been executed!")

# def task_b_func():  
#     print("Task B has been executed!")

# def task_c_func():  
#     print("Task C has been executed!")

# def task_d_func():  
#     print("Task D has been executed!")

def greet_with_name(name):
    print(f"Hello, {name}!")

def greet_with_name_city(name, city):
    print(f"Hello, {name} from {city}!")

with DAG(
    dag_id='executing_python_tasks',
    description = 'Python Operator in DAGs',
    default_args = default_args,
    start_date = days_ago(1),
    schedule_interval = timedelta(days=1),
    tags = ['tasks dependency', 'Downstream', 'Upstream', 'python scripts', 'arguments'],
) as dag:
    # this is the first task, by with keyword and this way we can avoid using the 'dag' parameter
    taskA = PythonOperator(
        task_id = 'task_a',
        python_callable = greet_with_name,
        op_kwargs = {'name': 'Tasneem Ahmed'}
    )

    taskB = PythonOperator(
        task_id = 'task_b',
        python_callable = greet_with_name_city,
        op_kwargs = {'name': 'Tasneem Ahmed', 'city': 'Karachi'}
    )
taskA >> taskB  # taskA is upstream of taskB

    # taskC = PythonOperator(
    #     task_id = 'task_c',
    #     python_callable = task_c_func,
    # )
    # taskD = PythonOperator(
    #     task_id = 'task_d',
    #     python_callable = task_d_func,
    # )

# taskA >> [taskB, taskC]  # taskA is upstream of taskB and taskC
# [taskB, taskC] >> taskD  # taskB and taskC are upstream of taskD