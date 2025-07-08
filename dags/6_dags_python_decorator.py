import pendulum

# Airflow 3.0 부터 아래 경로로 import 합니다.
from airflow.sdk import DAG, task

# Airflow 2.10.5 이하 버전에서 실습시 아래 경로에서 import 하세요.
#from airflow import DAG
#from airflow.decorators import task

with DAG(
    dag_id="6_dags_python_decorator",
    schedule=None,
    start_date=pendulum.datetime(2025, 7, 8, tz="Asia/Seoul"),
    catchup=False,
) as dag:
    
    @task(task_id="python_task_1")
    def print_context(some_input):
        print(some_input)

    python_task_1 = print_context('task_decorator 실행')

# [2025-07-08, 14:12:04] INFO - task_decorator 실행: chan="stdout": source="task"


    '''
    4번 파일과 비교해보자 @task를 사용하여 훨씬 간결해졌다.

    def select_fruit():
        fruit = ['APPLE','BANANA','ORANGE','AVOCADO']
        rand_int = random.randint(0,3)
        print("선택된 과일: ",fruit[rand_int])

    py_t1 = PythonOperator(
        task_id='py_t1',
        python_callable=select_fruit
    )

    py_t1
    
    '''