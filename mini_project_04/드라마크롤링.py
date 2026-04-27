import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

TARGET_OTTS = [
    "Netflix", "TVING", "Disney+", "Amazon Prime", "Hulu",
    "Apple TV", "Viki", "iQiyi", "WeTV", "Kocowa",
    "Wavve", "Coupang Play"
]

chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)

all_data = []
start_page = 1
end_page = 5  # 테스트 후 80으로 늘려주세요.

# ⭐ 순위 꼬임 방지를 위한 절대 카운터 변수 도입
global_rank = 1

print("🚀 크롤링을 시작합니다...")

try:
    for page in range(start_page, end_page + 1):
        list_url = f"https://mydramalist.com/search?adv=titles&ty=68&co=3&re=2021,2026&so=popular&page={page}"
        driver.get(list_url)
        print(f"\n📄 {page}페이지 목록 수집 중...")

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h6.title")))

        # 더 명확한 CSS Selector로 중복 링크 방지
        items = driver.find_elements(By.CSS_SELECTOR, "h6.text-primary.title a")
        page_links = []

        for item in items:
            title_text = item.text.strip()
            # 텍스트가 비어있는 가짜/숨김 링크는 패스
            if title_text:
                page_links.append({
                    'title': title_text,
                    'url': item.get_attribute('href'),
                    'rank': global_rank  # 1, 2, 3, 4 순서대로 강제 부여
                })
                global_rank += 1  # 하나 추가할 때마다 순위 1씩 증가

        for drama in page_links:
            try:
                print(f"🔍 [{drama['rank']}] {drama['title']} 수집 중...")
                driver.get(drama['url'])
                time.sleep(2)

                native_title = ""
                genres = ""
                tags = ""
                where_to_watch = ""

                # ⭐ 1. Native Title 추출 추가 ⭐
                try:
                    native_element = driver.find_element(By.XPATH,
                                                         "//li[contains(@class, 'list-item') and b[contains(text(), 'Native Title')]]")
                    native_title = native_element.text.replace("Native Title:", "").strip()
                except NoSuchElementException:
                    native_title = "정보 없음"

                # --- 2. Genres 추출 ---
                try:
                    genres_element = driver.find_element(By.XPATH,
                                                         "//li[contains(@class, 'list-item') and b[contains(text(), 'Genres')]]")
                    genres = genres_element.text.replace("Genres:", "").strip()
                except NoSuchElementException:
                    genres = "정보 없음"

                # --- 3. Tags 추출 ---
                try:
                    tags_element = driver.find_element(By.XPATH,
                                                       "//li[contains(@class, 'list-item') and b[contains(text(), 'Tags')]]")
                    tags = tags_element.text.replace("Tags:", "").replace("(Vote or add tags)", "").strip()
                except NoSuchElementException:
                    tags = "정보 없음"

                # --- 4. Where to Watch 추출 (필터링 유지) ---
                try:
                    raw_platforms = []
                    watch_box = driver.find_element(By.XPATH,
                                                    "//*[contains(text(), 'Where to Watch')]/ancestor::div[contains(@class, 'box') or contains(@class, 'col')]")
                    platforms = watch_box.find_elements(By.CSS_SELECTOR, "a")

                    for p in platforms:
                        b_tags = p.find_elements(By.TAG_NAME, "b")
                        if b_tags:
                            name = b_tags[0].text.strip()
                        else:
                            name = p.text.strip()

                        if not name:
                            imgs = p.find_elements(By.TAG_NAME, "img")
                            if imgs:
                                name = imgs[0].get_attribute("alt") or imgs[0].get_attribute("title")

                        if name:
                            raw_platforms.append(name)

                    filtered_platforms = set()
                    for raw_name in raw_platforms:
                        for target_ott in TARGET_OTTS:
                            if target_ott.lower() in raw_name.lower():
                                filtered_platforms.add(target_ott)
                                break

                    if filtered_platforms:
                        where_to_watch = ", ".join(list(filtered_platforms))
                    else:
                        where_to_watch = "정보 없음"

                except NoSuchElementException:
                    where_to_watch = "정보 없음"

                # 딕셔너리에 Native Title 포함 (입력된 순서대로 CSV 컬럼이 만들어집니다)
                all_data.append({
                    'Rank': drama['rank'],
                    'Title': drama['title'],
                    'Native Title': native_title,
                    'Genres': genres,
                    'Tags': tags,
                    'Where to Watch': where_to_watch
                })

            except Exception as inner_e:
                print(f"⚠️ [{drama['rank']}] 수집 에러 발생 후 넘어감: {inner_e}")
                continue

except Exception as e:
    print(f"❌ 치명적인 오류 발생: {e}")

finally:
    if all_data:
        df = pd.DataFrame(all_data)
        file_name = "MDL_Drama_Rankings_Final.csv"
        df.to_csv(file_name, index=False, encoding='utf-8-sig')
        print(f"\n✅ 수집 완료! 총 {len(df)}건의 데이터가 '{file_name}'에 저장되었습니다.")

        # 컬럼 순서가 맞게 들어갔는지 확인
        print("\n[데이터 미리보기]")
        print(df.head(3))
    else:
        print("😭 저장할 데이터가 없습니다.")

    driver.quit()