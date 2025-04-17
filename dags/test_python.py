'''
I was facing an issue which I have installed pandas in airflow-env but it was not being detected in the DAG and in airflow UI show 'ModuleNotFoundError: No module named 'pandas''.
I have tried to install pandas in the Airflow environment using pip, but it didn't work. 

Solution:
1. Check the Python environment used by Airflow:
    - Ensure that the Python environment where Airflow is running has pandas installed.
2. Use the correct Python executable: 
    - sudo /usr/bin/python3 -m pip install pandas
after know the path of the python executable which is used by Airflow /usr/bin/python3 because of panadas is not installed in the default python environment
install pandas in the Airflow environment using the correct Python executable.

'''
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys
import site

def print_environment_info():
    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version}")
    print(f"Site packages: {site.getsitepackages()}")
    
    try:
        import pandas
        print(f"Pandas version: {pandas.__version__}")
        print(f"Pandas location: {pandas.__file__}")
    except ImportError:
        print("Pandas is not installed in this environment")

with DAG(
    dag_id = 'environment_info',
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
) as dag:
    
    task = PythonOperator(
        task_id='print_environment_info',
        python_callable=print_environment_info,
    )