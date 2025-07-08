import pendulum

from airflow.sdk import DAG, task


with DAG(
    dag_id="13_dags_python_with_macro",
    schedule=None,
    start_date=pendulum.datetime(2025, 7, 8, tz="Asia/Seoul"),
    catchup=False
) as dag:  
    
    @task(task_id='task_using_macros',
      templates_dict={'start_date':'{{ (data_interval_end.in_timezone("Asia/Seoul") + macros.dateutil.relativedelta.relativedelta(months=-1, day=1)) | ds }}',
                      'end_date': '{{ (data_interval_end.in_timezone("Asia/Seoul").replace(day=1) + macros.dateutil.relativedelta.relativedelta(days=-1)) | ds }}'
     }
    )
    def get_datetime_macro(**kwargs):
        
        templates_dict = kwargs.get('templates_dict') or {}
        if templates_dict:
            start_date = templates_dict.get('start_date') or 'start_date없음'
            end_date = templates_dict.get('end_date') or 'end_date없음'
            print(start_date)
            print(end_date)


    @task(task_id='task_direct_calc')
    def get_datetime_calc(**kwargs):
        from dateutil.relativedelta import relativedelta

        data_interval_end = kwargs['data_interval_end']
        prev_month_day_first = data_interval_end.in_timezone('Asia/Seoul') + relativedelta(months=-1, day=1)
        prev_month_day_last = data_interval_end.in_timezone('Asia/Seoul').replace(day=1) +  relativedelta(days=-1)
        print(prev_month_day_first.strftime('%Y-%m-%d'))
        print(prev_month_day_last.strftime('%Y-%m-%d'))

    get_datetime_macro() >> get_datetime_calc()

    '''
    템플릿 매크로 방식
	•	DAG 정의부에서 바로 날짜 연산을 지정할 수 있어, BashOperator 등에서도 쉽게 활용 가능
	•	Jinja 템플릿 문법과 Airflow 내장 매크로를 활용해 DAG 파라미터, 환경 변수 등에 동적으로 날짜를 주입할 때 유용

	파이썬 직접 계산 방식
	•	복잡한 날짜 연산, 조건 분기, 추가 로직이 필요한 경우 코드로 직접 처리하는 것이 더 직관적
	•	함수 내에서 자유롭게 파이썬 라이브러리를 활용할 수 있음

    간단한 날짜 연산은 템플릿 매크로로, 복잡한 로직은 파이썬 코드로 처리하는 것이 일반적
    '''