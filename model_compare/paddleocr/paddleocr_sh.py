import logging
from paddleocr import PaddleOCR
from PIL import Image
import numpy as np
import json
import os

# PaddleOCR 디버그 로그 비활성화
logging.getLogger("ppocr").setLevel(logging.ERROR)

def save_json(dict):
    save_path = 'C:/Users/dnltj/OneDrive/바탕 화면/project/paddle_ocr/paddleocr_result'
    os.makedirs(save_path, exist_ok=True)  
    with open(os.path.join(save_path, 'paddle_result.json'), 'w+', encoding='utf-8') as json_file:
        json.dump(dict, json_file, ensure_ascii=False, indent=4)

def folder_or_img(path, func):
    temp_dict = {}

    if os.path.isdir(path):
        img_lst = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        for i in img_lst:
            recognition_lst, confidence_lst = func(os.path.join(path, i))
            temp_dict[os.path.basename(i)] = ''.join(recognition_lst)  # 리스트를 문자열로 병합하여 저장
            #print(f"Save {os.path.basename(i)}")

        save_json(temp_dict)

    else:
        recognition_lst, confidence_lst = func(path)
        temp_dict[os.path.basename(path)] = ''.join(recognition_lst)  # 리스트를 문자열로 병합하여 저장
        #print(f"Save {os.path.basename(path)}")

    save_json(temp_dict)

def detection(image_path):
    recognition_lst = []
    confidence_lst = []
    ocr = PaddleOCR(use_angle_cls=True, lang='korean')
    image = Image.open(image_path).convert('RGB')
    image_np = np.array(image)
    result = ocr.ocr(image_np, det=False, cls=True)
    for i in result[0]:
        #print(f"Save the result_{i[0]}")
        recognition_lst.append(i[0])
        confidence_lst.append(i[1])
    assert len(recognition_lst) == len(confidence_lst)
    return recognition_lst, confidence_lst

if __name__ == '__main__':
    path = 'C:/Users/dnltj/OneDrive/바탕 화면/project/paddle_ocr/word_images_split'
    folder_or_img(path, detection)
