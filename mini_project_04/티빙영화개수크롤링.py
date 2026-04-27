from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd


def crawl_movie_genres(prefix="MG", start=0, step=10):
    """
    start 번호부터 step(10)씩 증가하며 장르를 탐색하는 함수
    """
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless') # 과정 확인을 위해 주석 처리됨
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920x1080')

    print(f"🚀 [{prefix}] 계열 영화 장르 탐색을 시작합니다. (증가 폭: {step})")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    results = {}
    seen_titles = set()

    # 0부터 시작해서 10, 20, 30 ... 100, 110 순으로 증가
    index = start
    empty_count = 0
    MAX_EMPTY_LIMIT = 20  # 5번 연속 유효하지 않은 페이지가 나오면 종료

    while True:
        # 번호를 3자리 포맷으로 맞춤 (예: 0 -> 000, 10 -> 010, 100 -> 100)
        genre_code = f"{prefix}{index:03d}"
        url = f"https://www.tving.com/more/genre/{genre_code}"

        print(f"\n[{genre_code}] 접속 중: {url}")
        driver.get(url)
        time.sleep(3)  # 렌더링 대기

        # 1. 리다이렉트 확인
        if driver.current_url != url:
            print("⚠️ 유효하지 않은 주소 (리다이렉트). 다음 번호로 넘어갑니다.")
            empty_count += 1
            index += step  # 💡 10 증가
            if empty_count >= MAX_EMPTY_LIMIT:
                print(f"🛑 {MAX_EMPTY_LIMIT}번 연속 유효하지 않은 페이지 발생. 탐색 종료.")
                break
            continue

        # 2. 장르 제목 추출 및 검증
        try:
            title_xpath = '//*[@id="__next"]/main/section/div[1]/h2'
            title_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, title_xpath))
            )
            genre_title = title_element.text.strip()

            if not genre_title:
                print("⚠️ 제목 텍스트가 비어있음. 다음 번호로 넘어갑니다.")
                empty_count += 1
                index += step  # 💡 10 증가
                if empty_count >= MAX_EMPTY_LIMIT:
                    break
                continue

            if genre_title in seen_titles:
                print(f"🛑 중복된 장르명 발견: [{genre_title}] -> 더 이상 코드가 없다고 판단하여 탐색 종료.")
                break

            seen_titles.add(genre_title)
            empty_count = 0  # 정상 페이지 발견 시 카운트 초기화
            print(f"📌 발견된 장르명: [{genre_title}] - 스크롤 시작...")

        except TimeoutException:
            print("⚠️ 에러 페이지(제목 없음). 다음 번호로 넘어갑니다.")
            empty_count += 1
            index += step  # 💡 10 증가
            if empty_count >= MAX_EMPTY_LIMIT:
                break
            continue

        # 3. 무한 스크롤 진행
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # 4. 콘텐츠 개수 세기 (본문 img 태그 기준)
        img_elements = driver.find_elements(By.CSS_SELECTOR, "main img")
        count = len(img_elements)

        results[genre_title] = count
        print(f"✅ [{genre_title}] 수집 완료: {count}개")

        # 5. 다음 탐색을 위해 index를 10 증가
        index += step

    driver.quit()
    return results


def main():
    target_prefix = "MG"

    # 크롤링 실행 (MG000 부터 10씩 증가)
    final_data = crawl_movie_genres(prefix=target_prefix, start=0, step=10)

    # 결과 출력
    print("\n" + "=" * 40)
    print(f"📊 TVING [{target_prefix}] 계열 (영화) 자동 크롤링 최종 결과")
    print("=" * 40)
    for genre, count in final_data.items():
        print(f"{genre.ljust(15)} : {count}개")
    print("=" * 40)

    # DataFrame 변환, 필터링 및 CSV 저장
    if final_data:
        df = pd.DataFrame(list(final_data.items()), columns=['Genre', 'Content_Count'])

        # 💡 콘텐츠가 1개 이상인(0개가 아닌) 장르만 남기기
        df = df[df['Content_Count'] > 0]
        df = df.sort_values(by='Content_Count', ascending=False)

        if df.empty:
            print("\n⚠️ 수집된 콘텐츠가 1개 이상인 장르가 없어 CSV를 생성하지 않았습니다.")
        else:
            file_name = f"tving_movie_data_{target_prefix}.csv"
            df.to_csv(file_name, index=False, encoding='utf-8-sig')
            print(f"\n💾 0개인 장르를 제외하고 '{file_name}' 파일로 깔끔하게 저장되었습니다!")
    else:
        print("\n⚠️ 수집된 데이터가 없어 CSV 파일을 생성하지 않았습니다.")


if __name__ == "__main__":
    main()