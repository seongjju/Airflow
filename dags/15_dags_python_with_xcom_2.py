import pendulum

from airflow.sdk import DAG, task

with DAG(
    dag_id="15_dags_python_with_xcom_2",
    schedule=None,
    start_date=pendulum.datetime(2025, 7, 8, tz="Asia/Seoul"),
    catchup=False
) as dag:
    
    @task(task_id='python_xcom_push_by_return')
    def xcom_push_result(**kwargs):
        return 'Success'

    @task(task_id='python_xcom_pull_1')
    def xcom_pull_1(**kwargs):
        ti = kwargs['ti']
        value1 = ti.xcom_pull(task_ids='python_xcom_push_by_return')
        print('xcom_pull 메서드로 직접 찾은 리턴 값:' + value1)

    @task(task_id='python_xcom_pull_2')
    def xcom_pull_2(status, **kwargs):
        print('함수 입력값으로 받은 값:' + status)


    python_xcom_push_by_return = xcom_push_result()
    xcom_pull_2(python_xcom_push_by_return)
    python_xcom_push_by_return >> xcom_pull_1()

    '''
    2) Python 함수의 return 값 활용
    @Task 사용 시 함수 입, 출력 관계만으로도 >> 안쓰고도 순서 명확해짐 TaskFlow정의 됨

    return한 값은 자동으로 xcom에 key='return_value', task_ids=task_id로 저장됨
    
    xcom_push_result: INFO - Done. Returned value was: Success:
    xcom_pull_1: INFO - xcom_pull 메서드로 직접 찾은 리턴 값:Success:  
    xcom_pull_2: INFO - 함수 입력값으로 받은 값:Success: 

    '''


