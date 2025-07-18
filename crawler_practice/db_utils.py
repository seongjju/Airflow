# PostgreSQL 데이터베이스에 연결하기 위한 Python 라이브러리
import psycopg2
# 파이썬 내장 CSV 모듈
import csv
# 외부 설정 파일(config.py)에서 DB 연결 정보를 import
from config import DB_CONN
import logging

# DB 테이블 초기화 함수
def init_tables():
    # psycopg2를 사용해서 PostgreSQL에 연결
    # **DB_CONN은 앞서 import한 연결 정보 딕셔너리를 unpacking 해서 넘긴다.
    conn = psycopg2.connect(**DB_CONN)
    # SQL 초기화 스크립트(init_tables.sql)을 열어서 내용을 문자열로 읽는다.
    with open("/opt/airflow/crawler_practice/init_tables.sql", encoding="utf-8") as f:
        sql = f.read()
    # DB 작업을 수행하기 위한 커서를 생성
    cur = conn.cursor()
    # 위에서 읽은 SQL 내용을 실행하여 테이블을 생성
    cur.execute(sql)
    # 트랜잭션을 커밋해서 실제로 DB에 반영
    conn.commit()
    # 커서와 DB 연결을 닫음 -> 리소스를 정리
    cur.close()
    conn.close()
    logging.info("TABLE INIT 실행됨")

# DB에서 데이터를 추출해서 CSV로 저장하는 함수
def dump_top10_to_csv():
    output_path = "/opt/airflow/crawler_practice/news_top10.csv"
    conn = psycopg2.connect(**DB_CONN)
    cur = conn.cursor()
    cur.execute("SELECT * FROM news ORDER BY id LIMIT 10;")
    # 쿼리 결과를 모두 가져와서 리스트 형태로 저장
    rows = cur.fetchall()
    # 결과의 컬럼명들을 가져옴
	# cur.description은 열 정보가 들어 있는 속성
    colnames = [desc[0] for desc in cur.description]
    # newline은 라인 사이에 빈 줄이 생기는 걸 방지(Windows)
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        # CSV 쓰기 객체 생성
        writer = csv.writer(f)
        writer.writerow(colnames)
        writer.writerows(rows)
    cur.close()
    conn.close()
    logging.info(f"상위 10개 news 결과를 {output_path}로 저장 완료")