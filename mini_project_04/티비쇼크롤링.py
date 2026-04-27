import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# 타겟 OTT 리스트 (필터링용)
TARGET_OTTS = [
    "Netflix", "TVING", "Disney+", "Amazon Prime", "Hulu",
    "Apple TV", "Viki", "iQiyi", "WeTV", "Kocowa",
    "Wavve", "Coupang Play"
]

chrome_options = Options()
# chrome_options.add_argument("--headless")  # 화면 안 보이게 하려면 주석 해제
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)

all_data = []
start_page = 1
end_page = 5  # 테스트 완료 후 80 등 전체 페이지 수로 늘려주세요.

# 순위 꼬임 방지를 위한 전역 카운터
global_rank = 1

print("🚀 TV쇼(TV Shows) 크롤링을 시작합니다...")

try:
    for page in range(start_page, end_page + 1):
        # ⭐ TV쇼 전용 URL (ty=86)
        list_url = f"https://mydramalist.com/search?adv=titles&ty=86&co=3&re=2021,2026&so=popular&page={page}"
        driver.get(list_url)
        print(f"\n📄 {page}페이지 목록 수집 중...")

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h6.title")))

        # 정확한 제목 링크 요소만 추출
        items = driver.find_elements(By.CSS_SELECTOR, "h6.text-primary.title a")
        page_links = []

        for item in items:
            title_text = item.text.strip()
            if title_text:
                page_links.append({
                    'title': title_text,
                    'url': item.get_attribute('href'),
                    'rank': global_rank
                })
                global_rank += 1

        for tvshow in page_links:
            try:
                print(f"🔍 [{tvshow['rank']}] {tvshow['title']} 수집 중...")
                driver.get(tvshow['url'])
                time.sleep(2)

                native_title = ""
                genres = ""
                tags = ""
                where_to_watch = ""

                # 1. Native Title 추출
                try:
                    native_element = driver.find_element(By.XPATH,
                                                         "//li[contains(@class, 'list-item') and b[contains(text(), 'Native Title')]]")
                    native_title = native_element.text.replace("Native Title:", "").strip()
                except NoSuchElementException:
                    native_title = ""

                # 2. Genres 추출
                try:
                    genres_element = driver.find_element(By.XPATH,
                                                         "//li[contains(@class, 'list-item') and b[contains(text(), 'Genres')]]")
                    genres = genres_element.text.replace("Genres:", "").strip()
                except NoSuchElementException:
                    genres = ""

                # 3. Tags 추출
                try:
                    tags_element = driver.find_element(By.XPATH,
                                                       "//li[contains(@class, 'list-item') and b[contains(text(), 'Tags')]]")
                    tags = tags_element.text.replace("Tags:", "").replace("(Vote or add tags)", "").strip()
                except NoSuchElementException:
                    tags = ""

                # 4. Where to Watch 추출 및 필터링
                try:
                    raw_platforms = []
                    watch_box = driver.find_element(By.XPATH,
                                                    "//*[contains(text(), 'Where to Watch')]/ancestor::div[contains(@class, 'box') or contains(@class, 'col')]")
                    platforms = watch_box.find_elements(By.CSS_SELECTOR, "a")

                    for p in platforms:
                        b_tags = p.find_elements(By.TAG_NAME, "b")
                        name = b_tags[0].text.strip() if b_tags else p.text.strip()

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

                    where_to_watch = ", ".join(list(filtered_platforms)) if filtered_platforms else ""

                except NoSuchElementException:
                    where_to_watch = ""

                    # 데이터 담기
                all_data.append({
                    'Rank': tvshow['rank'],
                    'Title': tvshow['title'],
                    'Native Title': native_title,
                    'Genres': genres,
                    'Tags': tags,
                    'Where to Watch': where_to_watch
                })

            except Exception as inner_e:
                print(f"⚠️ [{tvshow['rank']}] 수집 에러 발생 후 넘어감: {inner_e}")
                continue

except Exception as e:
    print(f"❌ 치명적인 오류 발생: {e}")

finally:
    if all_data:
        df = pd.DataFrame(all_data)
        # ⭐ TV쇼 전용 파일명으로 저장
        file_name = "MDL_TVShow_Rankings_Final.csv"
        df.to_csv(file_name, index=False, encoding='utf-8-sig')
        print(f"\n✅ 수집 완료! 총 {len(df)}건의 데이터가 '{file_name}'에 저장되었습니다.")

        print("\n[데이터 미리보기]")
        print(df.head(5))
    else:
        print("😭 저장할 데이터가 없습니다.")

    driver.quit()