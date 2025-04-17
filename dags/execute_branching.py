from datetime import datetime, timedelta
from airflow.utils.dates import days_ago

# initiate DAG
from airflow import DAG

# this is first task
from airflow.operators.python import PythonOperator, BranchPythonOperator

default_args = {
    'owner' : 'tasneemahmed',
}
from random import choice
# this function completely randomize the output between True and False
def has_driving_license():
    return choice([True, False])
'''
branch function is used to determine which task to execute next based on the result of the previous task
if the previous task which check_license returns True, it will execute the eligible_for_license task
otherwise will execute not_eligible_for_license task
the task_id of the previous task is passed to the branch function using xcom_pull
the branch function checks the result of the previous task and returns the task_id of the next task to execute
this is done by using the return statement in the branch function
the return value of the branch function is used to determine which task to execute next
'''
def branch(ti):
    license_status = ti.xcom_pull(task_ids='check_license')
    if license_status == 'True':
        return 'eligible_for_license'
    else:
        return 'not_eligible_for_license'
def eligible():
    print("Eligible for driving license")
def not_eligible():
    print("Not eligible for driving license")

with DAG(
    dag_id='executing_Python_Branching_tasks',
    description = 'Python Operator in DAGs',
    default_args = default_args,
    start_date = days_ago(1),
    schedule_interval = timedelta(days=1),
    tags = ['tasks dependency', 'Branching', 'python scripts', 'X-comms'],
) as dag:
    # this is the first task, by with keyword and this way we can avoid using the 'dag' parameter
    check_license = PythonOperator(
        task_id = 'check_license',
        python_callable = has_driving_license,
    )
    branch_task = BranchPythonOperator(
        task_id = 'branch_task',
        python_callable = branch,
    )
    eligible_for_license = PythonOperator(
        task_id = 'eligible_for_license',
        python_callable = eligible,
    )
    not_eligible_for_license = PythonOperator(
        task_id = 'not_eligible_for_license',
        python_callable = not_eligible,
    )
check_license >> branch_task >> [eligible_for_license, not_eligible_for_license]
