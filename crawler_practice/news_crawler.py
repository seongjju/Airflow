from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import DB_CONN
import time
import psycopg2
import logging


# 기사 본문 아래에 나오는 기자 이름, 전문가 발언 등 추가정보 수집
# 찾을 수 없으면 except로 빠져나와 추가 정보 리스트 반환
def extract_additional_info(driver):
    texts = []
    index = 1
    while True:
        try:
            xpath = f'/html/body/div[1]/div[2]/div/div[1]/div[1]/div[2]/div[2]/p/span[{index}]'
            span = driver.find_element(By.XPATH, xpath)
            texts.append(span.text.strip())
            index += 1
        except:
            break
    return texts

# 뉴스 상세 페이지를 열고, 여러 정보를 크롤링
# 반환값은 딕셔너리: 작성시간, 수정시간, 기자명, 부제목, 추가정보
def crawl_news_detail(driver, url):
    driver.get(url)
    time.sleep(1)
    try:
        written = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/span').text.strip()
    except:
        written = "없음"

    try:
        modified = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div[1]/div[1]/div[3]/div[1]/div[2]/span').text.strip()
    except:
        modified = "없음"

    try:
        writer = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div[1]/div[1]/div[3]/div[2]/button/em').text.strip()
    except:
        try:
            writer = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div[1]/div[1]/div[3]/div[2]/a/em').text.strip()
        except:
            writer = None

    try:
        subtitle = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div[1]/div[2]/div[1]/article/strong').text.strip()
    except:
        subtitle = "없음"

    # 기자명이 없다면 그 아래 extract_additional_info() 호출해서 보충정보만 뽑음
    additional_info = extract_additional_info(driver) if not writer else []

    return {
        "작성시간": written,
        "수정시간": modified,
        "기자명": writer if writer else "없음",
        "부제목": subtitle,
        "추가정보": additional_info
    }

# 뉴스 특정 날짜(date)와 페이지 번호(page) 기반으로 크롤링 시작하는 메인 함수
def run_news_crawler_by_page(page=1, date="20250716"):
    # 드라이버는 함수 내부에서 열고, 마지막에 닫기
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    driver_path = "/usr/local/bin/chromedriver"
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 10)

    try:
        url = f"https://news.naver.com/main/list.naver?mode=LPOD&sid2=140&sid1=001&mid=sec&oid=001&isYeonhapFlash=Y&aid=0015510536&date={date}&page={page}"
        driver.get(url)
        time.sleep(2)

        article_urls = []
        for i in range(1, 10):
            try:
                xpath = f'/html/body/div[1]/table/tbody/tr/td[2]/div/div[2]/ul/li[{i}]/a[1]'
                elem = driver.find_element(By.XPATH, xpath)
                title = elem.text.strip()
                href = elem.get_attribute("href")
                article_urls.append((title, href))
            except:
                continue

        if not article_urls:
            logging.info(f"페이지 {page}: 뉴스 없음. 중단.")
            return

        for title, link in article_urls:
            detail = crawl_news_detail(driver, link)
            save_to_db(page, detail, title)  
            logging.info(f"\n제목: {title}")
            logging.info(f"부제목: {detail['부제목']}")
            logging.info(f"작성시간: {detail['작성시간']}")
            logging.info(f"수정시간: {detail['수정시간']}")
            logging.info(f"기자명: {detail['기자명']}")
            if detail["기자명"] == "없음" and detail["추가정보"]:
                logging.info("추가정보:")
                for t in detail["추가정보"]:
                    logging.info(" -", t)
    finally:
        driver.quit()

# 크롤링한 단일 기사 정보를 DB에 저장하는 함수
def save_to_db(page, detail, title):
    conn = psycopg2.connect(**DB_CONN)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO news (page, title, subtitle, written, modified, writer, extra)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        page,
        title,
        detail["부제목"],
        detail["작성시간"],
        detail["수정시간"],
        detail["기자명"],
        # 추가정보는 list이므로 "|"" 구분자로 문자열 결합해서 저장
        "|".join(detail.get("추가정보", []))
    ))
    conn.commit()
    cur.close()
    conn.close()