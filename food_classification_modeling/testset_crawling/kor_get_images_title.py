import json
import os
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright
from PIL import Image
import requests
from io import BytesIO

# JSON 파일 읽기
with open('product_data.json', 'r', encoding='utf-8') as f:
    gno_list = json.load(f)

# 이미지 저장 폴더 생성
if not os.path.exists('images'):
    os.makedirs('images')

base_url = "https://www.ewangmart.com/goods/detail.do?gno="

def save_image(image_url, title, count):
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            img_format = image_url.split('.')[-1] 
            img = Image.open(BytesIO(response.content))
            img_filename = f"images/{title}_{count}.{img_format}"
            img.save(img_filename)
            print(f"Saved image: {img_filename}")
        else:
            print(f"Failed to download image from {image_url} (Status Code: {response.status_code})")
    except Exception as e:
        print(f"Error saving image from {image_url}: {e}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    for gno in gno_list:
        if not gno:
            continue

        url = f"{base_url}{gno}"
        try:
            page.goto(url)
            # 제목 추출
            title = page.locator('.title.type2 span').inner_text().strip()
            print(f"Original Title extracted: {title}")

            # 이미지 추출
            images = page.locator('#detail-section1 img').element_handles()
            for index, img in enumerate(images):
                if index < 1:  
                    continue

                image_url = img.get_attribute('src')
                if image_url:
                    # 상대 경로일 경우 절대 경로로 변환
                    image_url = urljoin(url, image_url)
                    print(f"Processing image URL: {image_url}")  # 디버깅 메시지
                    save_image(image_url, title, index)

        except Exception as e:
            print(f"Error accessing URL {url}: {e}")

    browser.close()
