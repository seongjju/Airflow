import pendulum
from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import DAG

with DAG(
    dag_id="3_dags_bash_external",
    schedule=None,
    start_date=pendulum.datetime(2025, 7, 8, tz="Asia/Seoul"),
    catchup=False
) as dag:
    
    t1_orange = BashOperator(
        task_id="t1_orange",
        bash_command="/opt/airflow/plugins/shell/select_fruit.sh ORANGE",
    )

    t2_avocado = BashOperator(
        task_id="t2_avocado",
        bash_command="/opt/airflow/plugins/shell/select_fruit.sh AVOCADO",
    )

    t1_orange >> t2_avocado

    # dag 실행 전 chmod +x plugins/shell/select_fruit.sh으로 파일에 실행권한을 줘야 함
    # INFO - You selected Orange!
    # INFO - You selected other Fruit!