
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago

# initiate DAG
from airflow import DAG

# this is first task
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.models import Variable
import pandas as pd

from airflow.utils.task_group import TaskGroup
from airflow.utils.edgemodifier import Label

default_args = {
    'owner' : 'tasneemahmed',
}

# this is the path of the csv file,{0} is the name of the file I will specify later
output_file = '/home/tasneemahmed24/airflow/output/{0}.csv'

def read_csv_file(ti):
    df = pd.read_csv('/home/tasneemahmed24/airflow/dataset/insurance.csv')
    print(df)
    #return df.to_json()
    # By using return implicitly the df push to xcom, but if we want to push the df to xcom explicitly we can use xcom_push
    # this will push the df to xcom with the key 'read_csv' will can use this key to pull the df from xcom
    ti.xcom_push(key='read_csv', value=df.to_json())

# kwargs refer to recive number of arguments
def remove_null_values(ti):
    df = pd.read_json(ti.xcom_pull(key='read_csv'))
    filtered_df = df.dropna()
    print(filtered_df)
    #return filtered_df.to_json()
    # By using return implicitly the df push to xcom, but if we want to push the df to xcom explicitly we can use xcom_push
    ti.xcom_push(key='cleaned_data', value=filtered_df.to_json())

def branching():
    # this function is used to determine which task to execute varabile we created on Airflow UI>>Admin>>Variables: transform_action
    # Returns the value of default_var (None) if the variable is not set
    '''
    this function is used to determine which task to execute based on the value of the variable;
     this variable avilable across all the DAGs

    if the variable is set to filter_by_southeast, it will execute the filter_by_southeast task
    if the variable is set to filter_by_northeast, it will execute the filter_by_northeast task
    if the variable is set to filter_by_southwest, it will execute the filter_by_southwest task
    if the variable is set to filter_by_northwest, it will execute the filter_by_northwest task
    else it will execute the group_by_smoker_region_task

    - filtering & grouping refer to the task groups name where the tasks are defined
    '''

    transform = Variable.get("transform_action", default_var=None)
    if transform.startswith('filter'):
        return "filtering.{0}".format(transform)
    elif transform == 'group_by_smoker_region_task':
        return "grouping.{0}".format(transform)

def filter_by_southeast(ti):
    df = pd.read_json(ti.xcom_pull(key='cleaned_data'))
    filtered_df = df[df['region'] == 'southeast']
    print(filtered_df)
    filtered_df.to_csv(output_file.format('filtered_by_southeast'), index=False)
    
def filter_by_northeast(ti):
    df = pd.read_json(ti.xcom_pull(key='cleaned_data'))
    filtered_df = df[df['region'] == 'northeast']
    print(filtered_df)
    filtered_df.to_csv(output_file.format('filtered_by_northeast'), index=False)
    
def filter_by_southwest(ti):
    df = pd.read_json(ti.xcom_pull(key='cleaned_data'))
    filtered_df = df[df['region'] == 'southwest']
    print(filtered_df)
    filtered_df.to_csv(output_file.format('filtered_by_southwest'), index=False)
    
def filter_by_northwest(ti):
    df = pd.read_json(ti.xcom_pull(key='cleaned_data'))
    filtered_df = df[df['region'] == 'northwest']
    print(filtered_df)
    filtered_df.to_csv(output_file.format('filtered_by_northwest'), index=False)
    

def group_by_smoker_region(ti):
        # group by region or smoker and calculate mean of bmi, age and charges
    # and reset the index
    # this will create a new dataframe with the mean values of bmi, age and charges for each region
    # and the index will be reset to default integer index
    df = pd.read_json(ti.xcom_pull(key='cleaned_data'))
    grouped_df_smoker = df.groupby('smoker').agg(
        {'bmi': 'mean', 'age':'mean', 'charges': 'mean'}
        ).reset_index()
    print(grouped_df_smoker)
    grouped_df_smoker.to_csv(output_file.format('grouped_by_smoker'), index=False)

    grouped_df_region = df.groupby('region').agg(
        {'bmi': 'mean', 'age':'mean', 'charges': 'mean'}
        ).reset_index()
    print(grouped_df_region)
    grouped_df_region.to_csv(output_file.format('grouped_by_region'), index=False)


with DAG(
    dag_id='executing_Python_pipeline_using_variable',
    description = 'Run Python pipeline with branching using variable',
    schedule_interval = '@once',
    tags = ['python scripts', 'pipeline', 'branching', 'variable'],    
    default_args = default_args,
    start_date = days_ago(1),
)as dag:
    with TaskGroup("read_and_processing") as read_and_processing:
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
        # set dependency between the tasks in the task group : read_and_processing
        read_csv >> remove_null_values

    branch = BranchPythonOperator(
        task_id = 'branching_task',
        python_callable = branching,
    )
    with TaskGroup("filtering") as filtering:
        # this is the third task
        filter_by_southeast = PythonOperator(
            task_id = 'filter_by_southeast',
            python_callable = filter_by_southeast,
        )
        # this is the fourth task
        filter_by_northeast = PythonOperator(
            task_id = 'filter_by_northeast',
            python_callable = filter_by_northeast,
        )
        # this is the fifth task
        filter_by_southwest = PythonOperator(
            task_id = 'filter_by_southwest',
            python_callable = filter_by_southwest,
        )
        # this is the sixth task
        filter_by_northwest = PythonOperator(
            task_id = 'filter_by_northwest',
            python_callable = filter_by_northwest,
        )
    with TaskGroup("grouping") as grouping:
        # this is the seventh task
        group_by_smoker_region = PythonOperator(
            task_id = 'group_by_smoker_region_task',
            python_callable = group_by_smoker_region,
        )

# set the task dependencies
# Label refers to the label set on the edge
read_and_processing >> Label('Preprocessing Data') >> branch >> Label('Branch on Condition') >> [filtering, grouping]
                                     