import pendulum

from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import DAG

with DAG(
    dag_id="12_dags_bash_with_macro",
    schedule=None,
    start_date=pendulum.datetime(2025, 7, 8, tz="Asia/Seoul"),
    catchup=False
) as dag: 
    # START_DATE: 전월 말일, END_DATE: 1일 전
    bash_task_1 = BashOperator(
        task_id='bash_task_1',
        env={'START_DATE':'{{ data_interval_start.in_timezone("Asia/Seoul") | ds }}',
             'END_DATE':'{{ (data_interval_end.in_timezone("Asia/Seoul") - macros.dateutil.relativedelta.relativedelta(days=1)) | ds}}'
        }, 
        bash_command='echo "START_DATE: $START_DATE" && echo "END_DATE: $END_DATE"'
    )

    '''
    Airflow에서 macros의 역할
	•	Airflow는 Jinja 템플릿에서 날짜·시간 연산을 쉽게 할 수 있도록 파이썬의 dateutil 라이브러리의 relativedelta와 같은 도구를 macros로 제공
	•	DAG 내에서 날짜를 더하거나 빼는 등 다양한 날짜 연산을 템플릿 안에서 직접 할 수 있다.

    [2025-07-08, 16:09:41] INFO - START_DATE: 2025-07-08:
    [2025-07-08, 16:09:41] INFO - END_DATE: 2025-07-07:
    data_interval_end에서 1일을 빼서 전날 날짜를 구한다.
    
    xcom을 확인 해보면 Key: return_value, Value: END_DATE: 2025-07-07

    '''