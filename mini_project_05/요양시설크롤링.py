from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import re


def crawl_silvercare_user_logic(max_page=100):
    data_list = []

    options = webdriver.ChromeOptions()
    # options.add_argument('--headless') # 브라우저 창을 띄우지 않으려면 주석 해제
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    print("사용자 맞춤형 로직으로 크롤링을 시작합니다...")

    for page in range(1, max_page + 1):
        url = f"https://www.silvercarekorea.com/silver/list.php?pagenum={page}&addcode=26&searchkeyword=&orderby=count&hashtag=&gubun="

        try:
            driver.get(url)
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="body_main"]//table')))
            time.sleep(2)

            rows = driver.find_elements(By.XPATH, '//*[@id="body_main"]/table/tbody/tr')

            for row in rows:
                try:
                    # 해당 행의 모든 div를 가져옵니다.
                    divs = row.find_elements(By.XPATH, './td[2]/div')

                    # 기관명과 주소조차 없는 빈 줄은 건너뜁니다.
                    if len(divs) < 4:
                        continue

                    # 1. 기관명 (div[1])
                    name = divs[0].text.strip()

                    # 2. 주소 (div[2])
                    address = divs[1].text.strip()

                    # 💡 사용자님의 아이디어 적용: 3번째 방(div[3])에 '후기'가 있는지 검사
                    div3_text = divs[2].text.strip()

                    if '후기' in div3_text:
                        # 후기가 끼어있어서 뒤로 밀린 경우
                        cat_idx = 3  # 구분은 4번째 방(div[4])
                        info_idx = 4  # 정보는 5번째 방(div[5])
                    else:
                        # 평범한 구조인 경우
                        cat_idx = 2  # 구분은 3번째 방(div[3])
                        info_idx = 3  # 정보는 4번째 방(div[4])

                    # 인덱스 에러 방지 처리 후 텍스트 추출
                    category_text = divs[cat_idx].text.strip() if len(divs) > cat_idx else ""
                    info_text = divs[info_idx].text.strip() if len(divs) > info_idx else ""

                    # --- 텍스트 다듬기 ---
                    category = category_text.replace('구분', '').replace(':', '').replace('|', '').strip()

                    capacity = ""
                    caregiver = ""

                    # 정보란("/ 2008년 05월 개원 / 176 / 요양보호사 73") 파싱
                    if info_text:
                        parts = [p.strip() for p in info_text.split('/') if p.strip()]
                        for part in parts:
                            if '요양보호사' in part:
                                caregiver = re.sub(r'[^0-9]', '', part)  # 숫자만
                            elif '개원' in part or '설립' in part:
                                pass  # 개원일 정보는 무시
                            else:
                                nums = re.sub(r'[^0-9]', '', part)  # 숫자만
                                # 인원수라고 판단되는 경우만 (보통 4자리 이하 또는 '명' 포함)
                                if nums and (len(nums) <= 4 or '명' in part):
                                    capacity = nums

                    # 완성된 데이터 저장
                    data_list.append({
                        '기관명': name,
                        '주소': address,
                        '구분': category,
                        '정원(명)': capacity,
                        '요양보호사(명)': caregiver
                    })

                except Exception as e:
                    continue  # 한 행에서 에러가 나도 다음 행으로 계속 진행

            print(f"[{page}/{max_page}] 페이지 수집 완료")

        except Exception as e:
            print(f"페이지 로드 에러: {e}")
            break

    driver.quit()
    return pd.DataFrame(data_list)


# 실행 및 저장 (테스트로 3페이지)
df_silvercare_user = crawl_silvercare_user_logic(max_page=3)

if not df_silvercare_user.empty:
    print("\n[수집 결과 미리보기]")
    print(df_silvercare_user.head(10))
    df_silvercare_user.to_csv("busan_silvercare_user_logic.csv", index=False, encoding="utf-8-sig")
    print("\n'busan_silvercare_user_logic.csv' 저장 완료! 이제 구분이 완벽하게 들어올 것입니다.")