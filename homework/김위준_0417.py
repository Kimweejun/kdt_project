from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

query = input('검색할 키워드를 입력하세요: ')
print('--------------------------------------------------')

url = 'https://www.naver.com'
driver = webdriver.Chrome()
driver.get(url)
time.sleep(2)

search_box = driver.find_element(By.ID, "query")
search_box.send_keys(query)
search_box.send_keys(Keys.RETURN)
time.sleep(2)

# 블로그 탭 클릭 (작성하신 XPATH 유지)
driver.find_element(By.XPATH, '//*[@id="lnb"]/div[1]/div/div[1]/div/div[1]/div[5]/a').click()
time.sleep(3)

# 💡 수정된 부분: find_elements 사용 및 네이버 블로그 제목 a 태그 클래스('title_link') 적용
blog_elements = driver.find_elements(By.CLASS_NAME, 'title_link')

# 반복문을 통해 제목과 링크를 각각 추출합니다.
for element in blog_elements:
    title = element.text  # 텍스트(제목) 추출
    link = element.get_attribute('href')  # a 태그의 href 속성(링크 URL) 추출

    # 텍스트가 존재하는 유효한 데이터만 출력되도록 필터링
    if title:
        print(f'제목 : {title}')
        print(f'링크 : {link}')
        print('-' * 50)

# 크롤링 완료 후 브라우저 닫기 (선택 사항)
# driver.quit()