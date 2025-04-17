from datetime import datetime, timedelta
from airflow.utils.dates import days_ago

# initiate DAG
from airflow import DAG

# this is first task
from airflow.operators.python import PythonOperator

default_args = {
    'owner' : 'tasneemahmed',
}

def increment_by_one(number):
    print(f"Incrementing {number} by 1")
    return number + 1

#whenever operator is called in taskflow, it is task instance
# So ti refers to task instance
# confirm of task_ids match the task names defined below

def multiply_by_100(ti):
    number = ti.xcom_pull(task_ids='increment_task')
    print(f"Multiplying {number} by 100")
    return number * 100

def subtract_by_10(ti):
    number = ti.xcom_pull(task_ids='multiply_task')
    print(f"Subtracting 10 from {number}")
    return number - 10

def print_value(ti):
    number = ti.xcom_pull(task_ids='subtract_task')
    print(f"The final value is {number}")
    return number

with DAG(
    dag_id='executing_Python_Cross_Communication_tasks',
    description = 'Python Operator in DAGs',
    default_args = default_args,
    start_date = days_ago(1),
    schedule_interval = timedelta(days=1),
    tags = ['tasks dependency', 'Downstream', 'Upstream', 'python scripts', 'arguments', 'X-comms'],
) as dag:
    # this is the first task, by with keyword and this way we can avoid using the 'dag' parameter
    increment_by_1 = PythonOperator(
        task_id = 'increment_task',
        python_callable = increment_by_one,
        op_kwargs = {'number': 1},
    )
    multiple = PythonOperator(
        task_id = 'multiply_task',
        python_callable = multiply_by_100,
    )
    subtract = PythonOperator(
        task_id = 'subtract_task',
        python_callable = subtract_by_10,
    )
    print_value = PythonOperator(
        task_id = 'print_task',
        python_callable = print_value,
    )
    # taskA >> taskB  # taskA is upstream of taskB
    increment_by_1 >> multiple >> subtract >> print_value
    