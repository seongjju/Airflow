import pendulum
from common.common_func import regist

from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator

with DAG(
    dag_id="7_dags_python_with_op_args",
    schedule=None,
    start_date=pendulum.datetime(2025, 7, 8, tz="Asia/Seoul"),
    catchup=False
) as dag:
    
    regist_t1 = PythonOperator(
        task_id='regist_t1',
        python_callable=regist,
        op_args=['정성주','남자','한국항공대','27'],
    )

    regist_t1

    # [2025-07-08, 14:24:54] INFO - 이름: 정성주: chan="stdout": source="task"
    # [2025-07-08, 14:24:54] INFO - 성별: 남자: chan="stdout": source="task"
    # [2025-07-08, 14:24:54] INFO - 기타옵션들: ('한국항공대', '27'): chan="stdout": source="task"
    # [2025-07-08, 14:24:54] INFO - 기타옵션 중 두번째 값: 27: chan="stdout": source="tas