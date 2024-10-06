from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ChromeDriver 경로 설정
service = Service(executable_path='C:/Users/dnltj/OneDrive/문서/GitHub/OCR_Project/food_classification_modeling/fat_secret_data_crawling/etc/chromedriver.exe')

# 구글 플레이로 이동
driver = webdriver.Chrome(service=service)

# URL로 이동
url = "https://play.google.com/store/apps/details?id=com.fatsecret.android&hl=ko"
driver.get(url)  # driver.get() 사용

# 페이지 로딩 대기
time.sleep(2)

# 스크롤을 통해 요소를 화면에 보이게 함
scroll_count = 3  # 스크롤 횟수
for _ in range(scroll_count):
    driver.execute_script("window.scrollBy(0, 1000);")  # 아래로 1000픽셀 스크롤
    time.sleep(1)  # 스크롤 후 잠시 대기

# 리뷰 모두 보기 클릭
try:
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "span.VfPpkd-vQzf8d"))
    )
    button.click()

except Exception as e:
    print(f"버튼 클릭 중 오류 발생: {e}")

try:
    button_tt = driver.find_element(By.CSS_SELECTOR, value=button)
    button_tt.click()
except Exception as e:
    print(f"오류 발생: {e}")

time.sleep(2)  # 대기
driver.quit()  # 드라이버 종료


"""             
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
"""
