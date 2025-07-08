import pendulum

from airflow.sdk import DAG, task

with DAG(
    dag_id="10_dags_python_show_template",
    schedule="30 9 * * *",
    start_date=pendulum.datetime(2025, 7, 4, tz="Asia/Seoul"),
    catchup=True
) as dag: 
     
    @task(task_id='python_task')
    def show_templates(**kwargs):
        from pprint import pprint 
        pprint(kwargs)

    show_templates()  

    # 함수 내부에서 import를 하면 Airflow 스케줄러의 파싱 부하가 줄어들고, DAG 파일이 많을 때 전체 성능이 더 좋아진다.
    # 실행 시점에만 해당 모듈이 로드되기 때문
    # catchup=True이기 때문에, start_date 이후의 모든 스케줄링 시점에 대해 태스크가 실행됨 -> 4,5,6,7,8일 총 5개 Task 실행
    # Tip Akwargs는 "태스크 실행에 필요한 각종 정보"가 담긴 딕셔너리