import pendulum

from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import DAG


with DAG(
    dag_id="9_dags_bash_template",
    schedule=None,
    start_date=pendulum.datetime(2025, 7, 8, tz="Asia/Seoul"),
    catchup=False
) as dag:
    bash_t1 = BashOperator( 
        task_id='bash_t1', 
        bash_command='echo "data_interval_end: {{ data_interval_end }}  "'
    )

    bash_t2 = BashOperator(
        task_id='bash_t2',
        env={
            'START_DATE':'{{data_interval_start | ds }}',
            'END_DATE':'{{data_interval_end | ds }}'
        },
        bash_command='echo $START_DATE && echo $END_DATE'
    )

    bash_t1 >> bash_t2


    '''
    BashOperator는 bash_command, env 파라미터에만 Template 쓸 수 있음
    [2025-07-08, 14:39:38] INFO - data_interval_end: 2025-07-08 05:39:36.362000+00:00: source="airflow.task.hooks.airflow.providers.standard.hooks.subprocess.SubprocessHook"

    
    [2025-07-08, 14:39:39] INFO - 2025-07-08: source="airflow.task.hooks.airflow.providers.standard.hooks.subprocess.SubprocessHook"
    [2025-07-08, 14:39:39] INFO - 2025-07-08: source="airflow.task.hooks.airflow.providers.standard.hooks.subprocess.SubprocessHook"
    
    '''