from datetime import datetime, timedelta
from airflow.utils.dates import days_ago

# initiate DAG
from airflow import DAG

# this is first task
from airflow.operators.sqlite_operator import SqliteOperator

default_args = { 
    'owner' : 'tasneemahmed', 
}

with DAG( 
    dag_id='executing_sqlite_pipeline',
    description = 'Run SQLite pipeline',
    schedule_interval = '@once',
    tags = ['sqlite scripts', 'pipeline'],
    default_args = default_args,    
    start_date = days_ago(1),
)as dag:
    # this is the first task, by with keyword and this way we can avoid using the 'dag' parameter
    create_table = SqliteOperator(
        task_id = 'create_table_task',
        sqlite_conn_id = 'my_sqlite_conn', # which created in Airflow UI and connect to SQLite database: my_sqlite.db
        sql = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            email TEXT,
            city varchar(50),
            is_active BOOLEAN NOT NULL DEFAULT True,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );"""
        )
    # this is the second task
    insert_data_1 = SqliteOperator(
        task_id = 'insert_data_1',
        sqlite_conn_id = 'my_sqlite_conn',
        sql = """
        INSERT INTO users (name, age, is_active) VALUES
        ('John Doe', 30, True),
        ('Jane Smith', 25, True),
        ('Alice Johnson', 28, True),
        ('Bob Brown', 35, False),
        ('Charlie Black', 22, True);
        """
    )
    # this is the third task
    insert_data_2 = SqliteOperator(
        task_id = 'insert_data_2',
        sqlite_conn_id = 'my_sqlite_conn',
        sql = """
        INSERT INTO users (name, age) VALUES
        ('David White', 40),
        ('Eva Green', 29),
        ('Frank Blue', 33),
        ('Grace Yellow', 27),
        ('Hannah Purple', 31);
        """
    )
    # this is the fourth task
    delete_data = SqliteOperator(
        task_id = 'delete_data',
        sqlite_conn_id = 'my_sqlite_conn',
        sql = """
        DELETE FROM users WHERE is_active = False;
        """
    )
    # this is the fifth task
    update_data = SqliteOperator(
        task_id = 'update_data',
        sqlite_conn_id = 'my_sqlite_conn',
        sql = """update users set city = 'Cairo';"""
    )
   
    # this is the sixth task
    select_data = SqliteOperator(
        task_id = 'select_data',
        sqlite_conn_id = 'my_sqlite_conn',
        sql = """
        SELECT * FROM users;
        """,
        do_xcom_push = True # this will push the result of the query to XCom
    )
# this will run the first task and then run the second and third tasks in parallel,delete, update and finally run select_data
create_table >> [insert_data_1, insert_data_2] >> delete_data >> update_data >> select_data

