from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import json
import re

# Chrome WebDriver 설정
chrome_driver_path = "C:/Users/user/Desktop/project/testset_crawling/chromedriver-win64/chromedriver.exe"  ## chromedriver.exe파일 경로로 수정해주세요
service = Service(chrome_driver_path)

# cate ID 목록          14 : 유제품, 15 : 과자/안주
cate_ids = [14, 15]   ## 원하시는 카테고리로 번호 수정해주세요
all_products = []

for cate_id in cate_ids:
    driver = webdriver.Chrome(service=service)
    driver.get(f'https://www.ewangmart.com/goods/category.do?cate={cate_id}')
    wait = WebDriverWait(driver, 10)
    time.sleep(3)

    scroll_increment = 700

    while True:
        try:
            driver.execute_script(f"window.scrollBy(0, {scroll_increment});")
            time.sleep(1)
            # 더보기 클릭
            more_button = wait.until(EC.element_to_be_clickable((By.ID, 'pageBtn')))
            more_button.click()
            time.sleep(2)
        except Exception as e:
            print(f"Error during scrolling: {e}")
            break

    # 최상단으로 스크롤
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(2)

    # 모든 상품의 URL에서 gno(id) 값 추출
    pattern = r"gno=(\d+)"
    products = []

    product_elements = driver.find_elements(By.CSS_SELECTOR, '.thumb.type4 a') 
    for element in product_elements:
        url = element.get_attribute('href')
        gno = re.search(pattern, url).group(1) if re.search(pattern, url) else None
        if gno:
            products.append(gno)

    all_products.extend(products)  

    driver.quit()

# JSON으로 저장
with open("product_data.json", "w", encoding="utf-8") as json_file:
    json.dump(all_products, json_file, ensure_ascii=False, indent=4)
