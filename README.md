# Naver News Crawler with Apache Airflow

네이버 뉴스 페이지를 자동으로 크롤링하고, PostgreSQL DB에 저장한 후, 일부 데이터를 CSV/SQL로 추출하는 ETL 자동화 프로젝트
Apache Airflow를 사용하여 일련의 데이터 크롤링 및 저장 작업을 스케줄링/자동화


---

## 실행 방식

### 크롤링 워크플로우 (Airflow DAG)

**DAG ID**: `news_crawler_dag`

#### 흐름:

1. **DB 초기화**
2. **페이지별 뉴스 크롤링 (1~8)**  
3. **상위 10개 뉴스 CSV 저장**
4. **전체 news 테이블 SQL 백업**

### 사용 데이터베이스

- PostgreSQL 13
- news 테이블 구조는 `init_tables.sql`에 정의됨

---

## 주요 파일 설명

| 파일/디렉토리                      | 설명 |
|----------------------------------|------|
| `config/config.py`               | DB 접속 정보 (`DB_CONN`) 포함 |
| `crawler_practice/news_crawler.py` | Selenium 기반 기사 디테일 크롤링 |
| `crawler_practice/db_utils.py`  | init, CSV 저장 함수 정의 |
| `dags/news_crawler_dag.py`      | 전체 DAG 정의 파일 |
| `init_tables.sql`               | news 테이블 생성 SQL |
| `news_top10.csv`                | 상위 10개 기사 결과 CSV |
| `news_full.sql`                 | 전체 news 테이블 SQL 백업 |

---

## 결과

### CSV 일부
| id | page | title                                                          | subtitle                                      | written                   | modified                  | writer      | 
|----|------|----------------------------------------------------------------|-----------------------------------------------|---------------------------|---------------------------|-------------|
| 1  | 1    | 동네 한복판서 매몰사고라니…오산 옹벽붕괴에 주민 불안          | 시공·관리 정상이었는지 의문…추가붕괴 우려 속 더딘 사고수습 | 2025.07.16. 오후 11:38    | 2025.07.16. 오후 11:39    | 권준우 기자 |       |
| 2  | 1    | [긴급] 소방 오산 옹벽 붕괴사고 매몰자 1명 구조…심정지 상태    | 없음                                          | 2025.07.16. 오후 10:11    | 2025.07.16. 오후 10:12    | 류수현 기자 |       |
