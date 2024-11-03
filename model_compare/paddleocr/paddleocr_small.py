import logging
from paddleocr import PaddleOCR
from PIL import Image
import numpy as np
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# PaddleOCR 디버그 로그 비활성화 
logging.getLogger("ppocr").setLevel(logging.ERROR)

def save_json(data, filename='paddle_result.json'):
    save_path = 'C:/Users/user/Desktop/ocr/result_paddleocr'
    os.makedirs(save_path, exist_ok=True)
    with open(os.path.join(save_path, filename), 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

def process_image(image_path):
    # 각 스레드가 PaddleOCR 인스턴스를 별도로 생성
    ocr = PaddleOCR(use_angle_cls=True, lang='korean')
    image = Image.open(image_path).convert('RGB')
    result = ocr.ocr(np.array(image), det=False, cls=True)
    recognition_lst = ''.join([i[0] for i in result[0]])
    return os.path.basename(image_path), recognition_lst

def process_folder(path, limit=3000):
    temp_dict = {}
    img_paths = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(process_image, img_path): img_path for img_path in img_paths[:limit]}
        
        for i, future in enumerate(as_completed(futures), 1):
            try:
                filename, text = future.result()
                temp_dict[filename] = text
            except Exception as e:
                print(f"Error processing {futures[future]}: {e}")
                
            if i >= limit:
                print("3000개의 이미지를 처리했습니다. 프로그램을 종료합니다.")
                break

    save_json(temp_dict)

if __name__ == '__main__':
    path = 'C:/Users/user/Desktop/ocr/word_images_split'  # 적용할 파일 경로
    process_folder(path)
