from common.common_func import regist2
import pendulum

from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator

with DAG(
    dag_id="8_dags_python_with_op_kwargs",
    schedule=None,
    start_date=pendulum.datetime(2025, 7, 8, tz="Asia/Seoul"),
    catchup=False
) as dag:
    
    regist2_t1 = PythonOperator(
        task_id='regist2_t1',
        python_callable=regist2,
        op_args=['정성주','남자','한국항공대','27'],
        op_kwargs={'email':'koreatstm@naver.com','phone':'010'}
    )

    regist2_t1

    # kwargs는 키-값 형태로 
    '''
    regist2 함수 일부
    email = kwargs['email'] or None
    phone = kwargs['phone'] or None

    [2025-07-08, 14:29:15] INFO - 이름: 정성주: chan="stdout": source="task"
    [2025-07-08, 14:29:15] INFO - 성별: 남자: chan="stdout": source="task"
    [2025-07-08, 14:29:15] INFO - 기타옵션들: ('한국항공대', '27'): chan="stdout": source="task"

    키가 있을 때
    [2025-07-08, 14:29:15] INFO - koreatstm@naver.com: chan="stdout": source="task"
    [2025-07-08, 14:29:15] INFO - 010: chan="stdout": source="task

    키가 없을 때
    Task failed with exception: source="task"
    KeyError: 'phone'
    '''