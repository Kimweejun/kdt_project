from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import string  # A~Z 알파벳 생성을 위한 모듈


def process_page(driver, url, seen_titles):
    driver.get(url)
    time.sleep(3)  # 렌더링 대기
    if driver.current_url != url:
        print("⚠️ 유효하지 않은 주소 (리다이렉트).")
        return "INVALID", None, 0

    try:
        title_xpath = '//*[@id="__next"]/main/section/div[1]/h2'
        title_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, title_xpath))
        )
        genre_title = title_element.text.strip()

        if not genre_title:
            print("⚠️ 제목 텍스트가 비어있음.")
            return "INVALID", None, 0

        if genre_title in seen_titles:
            print(f"🛑 중복된 장르명 발견: [{genre_title}]")
            return "DUPLICATE", genre_title, 0

        seen_titles.add(genre_title)
        print(f"📌 발견된 장르명: [{genre_title}] - 스크롤 시작...")

    except TimeoutException:
        print("⚠️ 제목 요소를 찾을 수 없음 (에러 페이지).")
        return "INVALID", None, 0

    # 2. 무한 스크롤 진행
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # 3. 본문 영역 이미지 개수 세기
    img_elements = driver.find_elements(By.CSS_SELECTOR, "main img")
    count = len(img_elements)

    print(f"✅ [{genre_title}] 수집 완료: {count}개")
    return "SUCCESS", genre_title, count


def auto_crawl_tving_all(prefix="PCA"):
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless') # 눈으로 보려면 주석 처리
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920x1080')

    print(f"🚀 [{prefix}] 계열 장르 전체 탐색(숫자+알파벳)을 시작합니다...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    results = {}
    seen_titles = set()
    MAX_EMPTY_LIMIT = 10

    # ==========================================
    # Phase 1: 숫자 형태 탐색 (001, 002 ...)
    # ==========================================
    print("\n" + "=" * 30 + "\n[Phase 1] 숫자 코드 탐색 시작\n" + "=" * 30)
    index = 1
    empty_count = 0

    while True:
        url = f"https://www.tving.com/more/genre/{prefix}{index:03d}"
        status, title, count = process_page(driver, url, seen_titles)

        if status == "SUCCESS":
            empty_count = 0
            results[title] = count
        elif status == "INVALID":
            empty_count += 1
            if empty_count >= MAX_EMPTY_LIMIT:
                print(f"🛑 {MAX_EMPTY_LIMIT}번 연속 유효하지 않은 페이지 발생. 숫자 탐색 종료.")
                break
        elif status == "DUPLICATE":
            break  # 중복 발생 시 숫자 루프 즉시 종료

        index += 1

    print("\n" + "=" * 30 + "\n[Phase 2] 알파벳 코드 탐색 시작\n" + "=" * 30)
    empty_count = 0



    for char in string.ascii_uppercase:
        url = f"https://www.tving.com/more/genre/{prefix}{char}"
        status, title, count = process_page(driver, url, seen_titles)

        if status == "SUCCESS":
            empty_count = 0
            results[title] = count
        elif status == "INVALID":
            empty_count += 1
            if empty_count >= MAX_EMPTY_LIMIT:
                print(f"🛑 {MAX_EMPTY_LIMIT}번 연속 유효하지 않은 페이지 발생. 알파벳 탐색 종료.")
                break
        elif status == "DUPLICATE":
            continue
    driver.quit()
    return results


def main():
    target_prefix = "PCA"
    final_data = auto_crawl_tving_all(target_prefix)

    print("\n" + "=" * 40)
    print(f"📊 TVING [{target_prefix}] 계열 자동 크롤링 통합 최종 결과")
    print("=" * 40)
    for genre, count in final_data.items():
        print(f"{genre.ljust(15)} : {count}개")
    print("=" * 40)

    if final_data:
        df = pd.DataFrame(list(final_data.items()), columns=['Genre', 'Content_Count'])
        df = df.sort_values(by='Content_Count', ascending=False)

        file_name = f"tving_entertainment_data_{target_prefix}.csv"
        df.to_csv(file_name, index=False, encoding='utf-8-sig')
        print(f"\n💾 수집된 전체 데이터가 '{file_name}' 파일로 저장되었습니다!")
    else:
        print("\n⚠️ 수집된 데이터가 없어 CSV 파일을 생성하지 않았습니다.")


if __name__ == "__main__":
    main()
