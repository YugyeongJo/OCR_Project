import json
import os
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright #pip install playwright / python -m playwright install
from PIL import Image
import requests
from io import BytesIO
from googletrans import Translator #pip install googletrans==4.0.0-rc1
from collections import defaultdict


# JSON 파일 읽기
with open('product_data.json', 'r', encoding='utf-8') as f:
    gno_list = json.load(f)

# 이미지 저장 폴더 생성
if not os.path.exists('images'):
    os.makedirs('images')

base_url = "https://www.ewangmart.com/goods/detail.do?gno="

# Translator 인스턴스 생성
translator = Translator()

def save_image(image_url, title, count):
    try:
        response = requests.get(image_url)

        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            img_filename = f"images/{title}_{count}.jpg"
            img.save(img_filename, format = "JPG")
            print(f"Saved image: {img_filename}")
        else:
            print(f"Failed to download image from {image_url} (Status Code: {response.status_code})")

    except Exception as e:
        print(f"Error saving image from {image_url}: {e}")

#json으로 만들 dict
gno_names_dic = defaultdict()

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
            dict_title = title.replace(" ", "")
            print(f"Original Title extracted: {title}")

            translated_title = translator.translate(title, src='ko', dest='en').text
            translated_title = translated_title.replace(" ", "_") 
            gno_names_dic[dict_title] = translated_title, gno

            print(f"Translated Title: {translated_title}")

            # 이미지 추출
            images = page.locator('#detail-section1 img').element_handles()
            for index, img in enumerate(images):
                if index < 1: 
                    continue

                image_url = img.get_attribute('src')
                if image_url:
                    # 상대 경로일 경우 절대 경로로 변환
                    image_url = urljoin(url, image_url)
                    print(f"Processing image URL: {image_url}") 
                    save_image(image_url, translated_title, index)

                    with open("product_data_dict.json", "w", encoding="utf-8") as json_file:
                        json.dump(gno_names_dic, json_file, ensure_ascii=False, indent=4)

                    print("Product dictionary has been saved to product_data_dict.json")


        except Exception as e:
            print(f"Error accessing URL {url}: {e}")

    browser.close()
