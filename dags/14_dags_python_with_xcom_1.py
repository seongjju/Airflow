import pendulum

from airflow.sdk import DAG, task

with DAG(
    dag_id="14_dags_python_with_xcom_1",
    schedule=None,
    start_date=pendulum.datetime(2025, 7, 8, tz="Asia/Seoul"),
    catchup=False
) as dag:
    
    @task(task_id='python_xcom_push_task1')
    def xcom_push1(**kwargs):
        ti = kwargs['ti']
        ti.xcom_push(key="result1", value="value_1")
        ti.xcom_push(key="result2", value=[1,2,3])

    @task(task_id='python_xcom_push_task2')
    def xcom_push2(**kwargs):
        ti = kwargs['ti']
        ti.xcom_push(key="result1", value="value_2")
        ti.xcom_push(key="result2", value=[1,2,3,4])

    @task(task_id='python_xcom_pull_task')
    def xcom_pull(**kwargs):
        ti = kwargs['ti']
        value1 = ti.xcom_pull(key="result1", task_ids=['python_xcom_push_task1','python_xcom_push_task2']) 
        value2 = ti.xcom_pull(key="result2", task_ids='python_xcom_push_task1')
        print(value1)
        print(value2)


    xcom_push1() >> xcom_push2() >> xcom_pull()

    '''
    1) **kwargs에 존재하는 ti 객체 활용
    ti(TaskInstance)의 역할
	•	TaskInstance는 Airflow에서 개별 태스크의 실행 상태, 컨텍스트, 결과 등을 관리하는 핵심 객체
	•	태스크 실행 중에 XCom을 통해 데이터를 주고받거나, 실행 상태·메타데이터에 접근할 때 사용

    [2025-07-08, 16:21:08] INFO - ['value_1', 'value_2']: chan="stdout": source="task" key가 같으므로 리스트 형태로 둘 다 나옴
    [2025-07-08, 16:21:08] INFO - [1, 2, 3]: chan="stdout": source="task"
    xcom을 확인 해보면 Key: result1, Value: value_1
    xcom을 확인 해보면 Key: result2, Value: [1,2,3]
    xcom을 확인 해보면 Key: result1, Value: value_2
    xcom을 확인 해보면 Key: result2, Value: [1,2,3,4]


    '''