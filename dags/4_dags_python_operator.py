import pendulum
import random

from airflow.sdk import DAG
from airflow.operators.python import PythonOperator

with DAG(
    dag_id="4_dags_python_operator",
    schedule=None,
    start_date=pendulum.datetime(2025, 7, 8, tz="Asia/Seoul"),
    catchup=False
) as dag:
    
    def select_fruit():
        fruit = ['APPLE','BANANA','ORANGE','AVOCADO']
        rand_int = random.randint(0,3)
        print("선택된 과일: ",fruit[rand_int])

    py_t1 = PythonOperator(
        task_id='py_t1',
        python_callable=select_fruit
    )

    py_t1

    # [2025-07-08, 12:55:56] INFO - 선택된 과일:  AVOCADO: chan="stdout": source="task"
