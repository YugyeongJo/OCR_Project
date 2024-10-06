from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import csv
import time

# 구글플레이 리뷰 페이지로 이동
service = Service(executable_path='C:/Users/dnltj/OneDrive/문서/GitHub/OCR_Project/food_classification_modeling/fat_secret_data_crawling/etc/chromedriver.exe')

driver = webdriver.Chrome(service=service)
driver.get("https://play.google.com/store/apps/details?id=com.fatsecret.android&hl=ko")

# 리뷰 모두 보기 클릭
button = driver.find_element(By.CSS_SELECTOR, "span.VfPpkd-vQzf8d")
button.click()

# 페이지 스크롤해서 더 많은 리뷰 로드
SCROLL_PAUSE_TIME = 2
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # 페이지 끝까지 스크롤
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    # 스크롤 후 잠시 대기
    time.sleep(SCROLL_PAUSE_TIME)

    # 새로운 높이를 가져와서 비교
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# 리뷰 추출
review_elements = driver.find_elements(By.CLASS_NAME, 'UD7Dzf')  # 리뷰 텍스트가 있는 클래스 이름
reviews = [review.text for review in review_elements]  # 리스트에 리뷰 저장

# 리뷰를 CSV 파일로 저장
with open('reviews.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Review'])  # 헤더 추가
    for review in reviews:
        writer.writerow([review])  # 각 리뷰를 행으로 추가

# 드라이버 종료
driver.quit()
