from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time

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
    additional_info = extract_additional_info(driver) if not writer else []

    return {
        "작성시간": written,
        "수정시간": modified,
        "기자명": writer if writer else "없음",
        "부제목": subtitle,
        "추가정보": additional_info
    }

def run_news_crawler():
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
        date = "20250716"
        MAX_PAGE = 2  # 더 돌리고 싶으면 숫자만 고치면 됨
        base_url = "https://news.naver.com/main/list.naver"

        for page in range(1, MAX_PAGE + 1):
            print(f"\n 페이지 {page} 처리 중...")

            url = f"{base_url}?mode=LPOD&sid2=140&sid1=001&mid=sec&oid=001&isYeonhapFlash=Y&aid=0015510536&date={date}&page={page}"
            driver.get(url)
            time.sleep(2)

            # 뉴스 리스트 수집 (제목, 상세URL)
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
                print("뉴스 없음. 이 페이지에서 종료합니다.")
                break

            # 상세 기사 크롤링
            for title, link in article_urls:
                detail = crawl_news_detail(driver, link)
                print(f"\n 제목: {title}")
                print(f"▶ 부제목: {detail['부제목']}")
                print(f" 작성시간: {detail['작성시간']}")
                print(f" 수정시간: {detail['수정시간']}")
                print(f" 기자명: {detail['기자명']}")
                if detail["기자명"] == "없음" and detail["추가정보"]:
                    print(" 추가정보:")
                    for t in detail["추가정보"]:
                        print(" -", t)
    finally:
        driver.quit()

if __name__ == "__main__":
    run_news_crawler()