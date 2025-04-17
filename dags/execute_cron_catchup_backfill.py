from datetime import datetime, timedelta
from airflow.utils.dates import days_ago

# initiate DAG
from airflow import DAG

from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator

default_args = {
    'owner' : 'tasneemahmed',
}

from random import choice
# this function completely randomize the output between True and False
def choose_branch():
    return choice([True, False])
def branch_func(ti):
    if ti.xcom_pull(task_ids='task_choice'):
        return 'task_c'
    else:
        return 'task_d'

def task_c_func():
    print("Task c is executed")

with DAG(
    dag_id='executing_Python_Branching_tasks_with_Backfill',
    description = 'Python Operator in DAGs',
    default_args = default_args,
    start_date = days_ago(5),
    schedule_interval = '0 */12 * * *',
    #catchup = True,
    tags = ['tasks dependency', 'Branching', 'python scripts', 'X-comms'],
) as dag:
    # this is the first task, by with keyword and this way we can avoid using the 'dag' parameter
    task_a = BashOperator(
        task_id = 'task_a',
        bash_command = 'echo Task A is executed',
    )
     # this is the second task
    task_b = PythonOperator(
        task_id = 'task_choice',
        python_callable = choose_branch,
    )
    # this is the third task
    branch = BranchPythonOperator(
        task_id = 'branch_task',
        python_callable = branch_func,
    )

    task_c = PythonOperator(
        task_id = 'task_c',
        python_callable = task_c_func,
    )
    task_d = BashOperator(
        task_id = 'task_d',
        bash_command = 'echo Task D is executed',
    )
    task_a >> task_b >> branch >> [task_c, task_d]   

