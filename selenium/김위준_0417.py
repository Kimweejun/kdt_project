from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pandas as pd


query = input('검색할 키워드를 입력하세요: ').strip(' ')
print('--------------------------------------------------')

url = 'https://www.naver.com'
driver = webdriver.Chrome()
driver.get(url)
time.sleep(2)

search_box = driver.find_element(By.ID,"query")
search_box.send_keys(query)
search_box.send_keys(Keys.RETURN)
time.sleep(2)

driver.find_element(By.XPATH,'//*[@id="lnb"]/div[1]/div/div[1]/div/div[1]/div[5]/a').click()
time.sleep(3)

blog_titles = driver.find_elements(By.CLASS_NAME,'sds-comps-text-type-headline1')

lst = []

for i in blog_titles:
    title = i.text
    link_element = i.find_element(By.XPATH, './ancestor::a')
    link = link_element.get_attribute('href')
    lst.append([title,link])
    print(f'제목: {title}')
    print(f'링크: {link}')
    print('--------------------------------------------------')


df = pd.DataFrame(lst, columns=['제목', '링크'])
df.to_csv(f'naver_{query}.csv', index=False)
