from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By

# html 정보를 입력해서 객체(버튼/입력창 등) 선택
# find_element(By.ID)
# find_element(By.CLASS_NAME)
# find_element(By.XPATH)
# find_element(By.)



driver = webdriver.Chrome()
driver.get("http://www.google.co.kr/")
time.sleep(5)

# search_box = driver.find_element(By.CLASS_NAME, "gLFyf")
search_box = driver.find_element(By.XPATH, '//*[@id="APjFqb"]')
search_box.send_keys("파이썬")
search_box.send_keys(Keys.RETURN)

time.sleep(5)
driver.quit()
