import pendulum

from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import DAG, Variable

with DAG(
    dag_id="18_dags_bash_with_variable",
    schedule=None,
    start_date=pendulum.datetime(2025, 7, 8, tz="Asia/Seoul"),
    catchup=False
) as dag:
    var_value = Variable.get("sample_key") 

    bash_var_1 = BashOperator(
    task_id="bash_var_1",
    bash_command=f"echo variable:{var_value}"
    )

    bash_var_2 = BashOperator(
    task_id="bash_var_2",
    bash_command="echo variable:{{var.value.sample_key}}"
    )

    '''
    xcom은 특정 dag, schedule에 수행되는 Task간에만 공유됨. 모든 dag이 공유하는 전역 변수
    ui에 Admin-Variables에 올바른 key,value를 넣으면 됨
    두 task의 결과 모두
    INFO - variable:sample_key입니다.
    '''