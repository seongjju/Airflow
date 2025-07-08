import pendulum

from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import DAG

with DAG(
    dag_id="16_dags_bash_with_xcom",
    schedule=None,
    start_date=pendulum.datetime(2025, 7, 8, tz="Asia/Seoul"),
    catchup=False
) as dag:
    bash_push = BashOperator(
    task_id='bash_push',
    bash_command="echo START && "
                 "echo XCOM_PUSHED "
                 "{{ ti.xcom_push(key='bash_pushed',value='first_bash_message') }} && "
                 "echo COMPLETE"
    )

    bash_pull = BashOperator(
        task_id='bash_pull',
        env={'PUSHED_VALUE':"{{ ti.xcom_pull(key='bash_pushed', task_ids='bash_push') }}",
            'RETURN_VALUE':"{{ ti.xcom_pull(task_ids='bash_push') }}"},
        bash_command="echo $PUSHED_VALUE && echo $RETURN_VALUE ",
        do_xcom_push=False # xcom에 넣지 않겠다는 뜻, python과 달리 ti를 따로 꺼내지 않고 바로 ti.xcom~~
    )

    bash_push >> bash_pull

    '''
    BashOperator는 Template 되는 두 파라미터에 Template 사용하여 push, pull
    
    -  bash_push
    INFO - START: 
    INFO - XCOM_PUSHED None:
    INFO - COMPLETE: 
    INFO - Command exited with return code 0: 

    -  bash_pull
    INFO - COMPLETE: 만 나오게 되는데, 마지막 출력문만 자동으로 return_value에 저장되기 때문

    key: bash_pushed, value: first_bash_message
    key: return_value, value: COMPLETE

    '''