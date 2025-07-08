import pendulum
from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import DAG

with DAG(
    dag_id="1_dags_bash_operator",
    schedule="0 0 * * *", #분 시 일 월 요일
    start_date=pendulum.datetime(2025, 7, 8, tz="Asia/Seoul"),
    catchup=False
) as dag:
    bash_t1 = BashOperator(
        task_id="bash_t1",
        bash_command="echo whoami",
    )

    bash_t2 = BashOperator(
        task_id="bash_t2",
        bash_command="echo $HOSTNAME; echo good",
    )

    bash_t3 = BashOperator(
        task_id="bash_t3",
        bash_command="echo $HOSTNAME; echo good",
    )

    bash_t4 = BashOperator(
        task_id="bash_t4",
        bash_command="echo $HOSTNAME; echo good",
    )

    bash_t1 >> bash_t2 >> bash_t3 >> bash_t4


'''
[2025-07-08, 12:02:08] INFO - Pushing xcom: ti="RuntimeTaskInstance(id=UUID(), task_id='bash_t2', dag_id='dags_bash_operator', run_id='manual__2025-07-08T03:02:05.037061+00:00', try_number=1, map_index=-1, hostname='', context_carrier={}, task=<Task(BashOperator): bash_t2>, bundle_instance=LocalDagBundle(name=dags-folder), max_tries=0, start_date=datetime.datetime(2025, 7, 8, 3, 2, 8, 551411, tzinfo=TzInfo(UTC)), end_date=None, state=<TaskInstanceState.RUNNING: 'running'>, is_mapped=False, rendered_map_index=None)": source="task"
dag_id는 trigger냐 정해진 일정이냐에 따라 나뉨, 이건 수동실행했기에 manual

INFO - whoami:
INFO - 769890e730d0:
INFO - good:


'''