import pendulum

from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import DAG, task

with DAG(
    dag_id="17_dags_bash_python_with_xcom",
    schedule=None,
    start_date=pendulum.datetime(2025, 7, 8, tz="Asia/Seoul"),
    catchup=False
) as dag:

    @task(task_id='python_push')
    def python_push_xcom():
        result_dict = {'status':'Good','data':[1,2,3],'options_cnt':100}
        return result_dict

    bash_pull = BashOperator(
        task_id='bash_pull',
        env={
            'STATUS':'{{ti.xcom_pull(task_ids="python_push")["status"]}}',
            'DATA':'{{ti.xcom_pull(task_ids="python_push")["data"]}}',
            'OPTIONS_CNT':'{{ti.xcom_pull(task_ids="python_push")["options_cnt"]}}'
        },
        bash_command='echo $STATUS && echo $DATA && echo $OPTIONS_CNT'
    )
    python_push_xcom() >> bash_pull

    '''
    xcom을 확인해보면 
    bash_pull Task의 key: return_value, value:100
    python_push Task의 key: return_value, value:{'data': [1, 2, 3], 'status': 'Good', 'options_cnt': 100}

    - bash_pull
    INFO - Good: 
    INFO - [1, 2, 3]:
    INFO - 100:

    '''

    bash_push = BashOperator(
    task_id='bash_push',
    bash_command='echo PUSH_START '
                 '{{ti.xcom_push(key="bash_pushed",value=200)}} && '
                 'echo PUSH_COMPLETE'
    )
    # echo가 2개지만 마지막 출력문만 return으로 간주되어 xcom에 저장된다.

    @task(task_id='python_pull')
    def python_pull_xcom(**kwargs):
        ti = kwargs['ti']

        status_value = ti.xcom_pull(key='bash_pushed', task_ids='bash_push')
        return_value = ti.xcom_pull(task_ids='bash_push')
        print('status_value:' + str(status_value))
        print('return_value:' + return_value)

    bash_push >> python_pull_xcom()

    '''
    Airflow의 @task 데코레이터나 PythonOperator는 태스크 함수가 반환하는 값을 자동으로 XCom에 push

    xcom을 확인해보면 
    bash_push Task의 key: return_value, value:PUSH_COMPLETE
    bash_push Task의 key: bash_pushed, value:200

    - bash_push
    INFO - PUSH_START None:
    INFO - PUSH_COMPLETE:

    - python_pull
    INFO - status_value:200: 
    INFO - return_value:PUSH_COMPLETE: 
    '''