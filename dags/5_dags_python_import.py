import pendulum
from common.common_func import get_sftp

from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator


with DAG(
    dag_id="5_dags_python_import",
    schedule=None,
    start_date=pendulum.datetime(2025, 7, 8, tz="Asia/Seoul"),
    catchup=False
) as dag:

    task_get_sftp = PythonOperator(
        task_id='task_get_sftp',
        python_callable=get_sftp
    )

    # .env에 "PYTHONPATH=/opt/airflow/plugins" 필요
    # [2025-07-08, 14:00:31] INFO - sftp 작업을 시작합니다: chan="stdout": source="task"
