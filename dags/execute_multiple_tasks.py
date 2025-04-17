

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
    dag_id='executing_multiple_tasks',
    description = 'DAG with multiple tasks and dependencies',
    default_args = default_args,
    start_date = days_ago(1),
    schedule_interval = timedelta(days=1),
    tags = ['bach', 'tasks dependency', 'Downstream', 'Upstream', 'bash scripts'],
    template_searchpath = '/home/tasneemahmed24/airflow/dags/bash_scripts',
) as dag:

    # this is the first task, by with keyword and this way we can avoid using the 'dag' parameter
    taskA = BashOperator(
        task_id = 'task_a',
        bash_command = 'taskA.sh'
    )

    taskB = BashOperator(
        task_id = 'task_b',
        bash_command = 'taskB.sh'
    )

    taskC = BashOperator(
        task_id = 'task_c',
        bash_command = 'taskC.sh'
    )

    taskD = BashOperator(
        task_id = 'task_d',
        bash_command = 'taskD.sh'
    )

    taskE = BashOperator(
        task_id = 'task_e',
        bash_command = 'taskE.sh'
    )

    taskF = BashOperator(
        task_id = 'task_f',
        bash_command = 'taskF.sh'
    )
    # this is the last task
    taskG = BashOperator(
        task_id = 'task_g',
        bash_command = 'taskG.sh'
    )

    # set task dependencies using BigShift operator
    # run taskA then taskB and taskE
    taskA >> taskB >> taskE
    # run taskA then taskC and taskF    
    taskA >> taskC >> taskF
    # run taskA then taskD and taskG
    taskA >> taskD >> taskG


    # set task dependencies using BitShift operator
    # run taskA before taskB and taskC
    #taskA >> [taskB, taskC]
    # run taskB and taskC before taskD
    #[taskB, taskC] >> taskD

    # run taskA before taskB and taskC
    #taskA.set_downstream([taskB, taskC])
    # run taskB and taskC before taskD
    #[taskB, taskC].set_downstream(taskD)


