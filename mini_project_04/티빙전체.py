from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


def get_total_drama_count():
    # 1. 크롬 드라이버 설정
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless') # 화면을 숨기려면 주석(#) 해제
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920x1080')

    print("🚀 '드라마 전체(PCA)' 크롤링을 시작합니다...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # 2. 타겟 URL 접속 (새로운 탭/창으로 열림)
    target_url = "https://www.tving.com/more/genre/PCA"
    print(f"접속 중: {target_url}")
    driver.get(target_url)

    # 페이지 및 이미지 초기 로딩 대기
    time.sleep(3)

    print("📌 무한 스크롤을 진행하여 모든 콘텐츠를 불러옵니다...")

    # 3. 무한 스크롤 진행
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # 스크롤을 브라우저 맨 아래로 내림
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # 이미지 로딩 대기

        # 스크롤 후 새로운 화면 높이 계산
        new_height = driver.execute_script("return document.body.scrollHeight")

        # 더 이상 스크롤이 내려가지 않으면 완료
        if new_height == last_height:
            break
        last_height = new_height

    # 4. 본문 영역(main)의 포스터 이미지(img) 개수 카운트
    img_elements = driver.find_elements(By.CSS_SELECTOR, "main img")
    total_count = len(img_elements)

    # 브라우저 종료
    driver.quit()

    # 5. 결과 출력
    print("\n" + "=" * 40)
    print(f"✅ [드라마 전체 (PCA)] 총 콘텐츠 개수: {total_count}개")
    print("=" * 40)


if __name__ == "__main__":
    get_total_drama_count()