import pendulum

from airflow.sdk import DAG, task
from airflow.providers.standard.operators.python import PythonOperator

with DAG(
    dag_id="11_dags_python_template",
    schedule=None,
    start_date=pendulum.datetime(2025, 7, 8, tz="Asia/Seoul"),
    catchup=False
) as dag:
    
    def python_function1(start_date, end_date, **kwargs):
        print(start_date)
        print(end_date)

    python_t1 = PythonOperator(
        task_id='python_t1',
        python_callable=python_function1,
        op_kwargs={'start_date':'{{data_interval_start | ds}}', 'end_date':'{{data_interval_end | ds}}'}
    )

    @task(task_id='python_t2')
    def python_function2(**kwargs):
        print(kwargs)
        print('ds:' + kwargs['ds'])
        print('ts:' + kwargs['ts'])
        print('data_interval_start:' + str(kwargs['data_interval_start']))
        print('data_interval_end:' + str(kwargs['data_interval_end']))
        print('task_instance:' + str(kwargs['ti']))


    python_t1 >> python_function2()


    '''
    Python Operator는 python_callable, op_kwargs, op_args, templates_dict, templates_exts, show_return_value_in_logs 파라미터에만 Template 쓸 수 있음
    **kwargs에 Template 변수들을 자동으로 제공함

    [2025-07-08, 15:55:03] INFO - 2025-07-08: chan="stdout": source="task"
    [2025-07-08, 15:55:03] INFO - 2025-07-08: chan="stdout": source="task"

    [2025-07-08, 15:55:04] INFO - ds:2025-07-08: chan="stdout": source="task"
    [2025-07-08, 15:55:04] INFO - ts:2025-07-08T06:55:01.299000+00:00: chan="stdout": source="task"
    [2025-07-08, 15:55:04] INFO - data_interval_start:2025-07-08 06:55:01.299000+00:00: chan="stdout": source="task"
    [2025-07-08, 15:55:04] INFO - data_interval_end:2025-07-08 06:55:01.299000+00:00: chan="stdout": source="task"
    [2025-07-08, 15:55:04] INFO - task_instance:id=UUID('0197e8d1-05f2-78f8-8008-85bfd2b108a7') ~~
    '''