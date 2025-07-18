from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator
from db_utils import init_tables, dump_top10_to_csv
from news_crawler import run_news_crawler_by_page
from datetime import datetime
from config import DB_CONN
from docker.types import Mount
import psycopg2
import os
from crawler_practice import news_crawler

default_args = {"start_date": datetime(2025, 7, 16)}

# DAG 컨텍스트 블록 시작
with DAG(
    dag_id='news_crawler_dag',
    default_args=default_args,
    schedule=None,
    catchup=False,
    tags=["naver", "news", "paging"]
) as dag:

    init_db_task = PythonOperator(
        task_id='init_tables',
        python_callable=init_tables
    )

    prev = init_db_task
    for page in range(1, 9):
        t = PythonOperator(
            task_id=f"crawl_page_{page}",
            python_callable=run_news_crawler_by_page,
            op_kwargs={"page": page}
        )
        # Task 간 순차적으로 실행되도록 prev >> t 로 체이닝
        prev >> t
        prev = t

    dump_csv_task = PythonOperator(
        task_id='dump_top10_to_csv',
        python_callable=dump_top10_to_csv
    )

    # DockerOperator: news 테이블 SQL 덤프
    dump_sql_task = DockerOperator(
        task_id='dump_news_sql',
        image='postgres:13',
        command=(
            # pg_dump: news테이블만 SQL 파일로 백업
            "pg_dump -h {host} -U {user} -d {db} -t news -Fp "
            "-f /app/crawler_practice/news_full.sql"
        ).format(
            host=DB_CONN['host'],
            user=DB_CONN['user'],
            db=DB_CONN['dbname']
        ),
        environment={
            'PGPASSWORD': DB_CONN['password']
        },
        # mounts: /app/crawler_practice 안에 news_full.sql 저장되도록 로컬 디렉토리를 공유
        mounts=[
            Mount(
                source="/Users/seongjujeong/Desktop/crawler_practice/crawler_practice",
                target="/app/crawler_practice",
                type="bind"
            )
        ],
        auto_remove="success",
        mount_tmp_dir=False,
        network_mode="crawler_practice_default"
        
    )

    prev >> dump_csv_task >> dump_sql_task