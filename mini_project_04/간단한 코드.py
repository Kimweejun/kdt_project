from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

driver = webdriver.Chrome()
results = {}

urls = [f"https://www.tving.com/more/genre/PCA{i:03d}" for i in range(1, 10)]

for url in urls:
    driver.get(url)
    time.sleep(3)
    title = driver.find_element(By.XPATH, '//h2').text

    while True:
        last_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        if last_height == driver.execute_script("return document.body.scrollHeight"):
            break
    count = len(driver.find_elements(By.CSS_SELECTOR, "main img"))
    results[title] = count

driver.quit()
df = pd.DataFrame(results.items(), columns=['Genre', 'Count'])
df.to_csv("tving_data.csv", index=False, encoding='utf-8-sig')

