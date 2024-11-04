import logging
import json
import os
from paddleocr import PaddleOCR
from PIL import Image, UnidentifiedImageError
import numpy as np
from tqdm import tqdm
import paddle

"""
pip install paddlepaddle
pip install paddleocr
주의 : 파일명이 paddleocr과 같다면 오류발생합니다.
"""

# PaddleOCR 디버그 로그 비활성화
logging.getLogger("ppocr").setLevel(logging.ERROR)

def initialize_ocr(lang='korean', use_gpu=True):
    """PaddleOCR 모델 초기화"""
    return PaddleOCR(use_angle_cls=True, lang=lang, use_gpu=use_gpu)

def process_images_in_batches(image_files, ocr, batch_size=10):
    """이미지 파일을 배치로 처리하고 결과를 반환하는 함수"""
    results_dict = {}
    total_batches = (len(image_files) + batch_size - 1) // batch_size

    for i in tqdm(range(total_batches), desc="Processing images"):
        batch_files = image_files[i * batch_size : (i + 1) * batch_size]
        for image_file in batch_files:
            try:
                recognition_lst, _ = detection(ocr, image_file)
                results_dict[os.path.basename(image_file)] = ''.join(recognition_lst)
            except Exception as e:
                print(f"Error processing {image_file}: {e}")

    return results_dict

def save_results_to_json(results_dict, output_path):
    """결과를 JSON 파일로 저장하는 함수"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w+", encoding="utf-8") as json_file:
        json.dump(results_dict, json_file, ensure_ascii=False, indent=4)

def detection(ocr, image_path):
    """OCR 인식 수행"""
    recognition_lst = []
    try:
        image = Image.open(image_path).convert('RGB')
    except UnidentifiedImageError:
        print(f"Error: Cannot identify image file {image_path}")
        return [], []
    except Exception as e:
        print(f"Unexpected error opening image {image_path}: {e}")
        return [], []
    
    image_np = np.array(image)
    try:
        result = ocr.ocr(image_np, det=False, cls=True)
        recognition_lst = [i[0] for i in result[0]]
    except Exception as e:
        print(f"Error during OCR processing for {image_path}: {e}")
        return [], []

    return recognition_lst, []  

if __name__ == '__main__':
    # GPU 사용 여부 확인 및 설정
    use_gpu = paddle.device.is_compiled_with_cuda() and paddle.device.cuda.device_count() > 0
    #print(f"Using GPU: {use_gpu}")

    # 위치 설정
    image_folder_path = '/content/drive/MyDrive/SeSac/images'  # 이미지 폴더 경로
    output_folder = '/content/drive/MyDrive/SeSac/result_paddleocr'  # 결과를 저장할 경로
    output_json_path = os.path.join(output_folder, 'paddle_result.json')
    batch_size = 32  

    ocr = initialize_ocr(use_gpu=use_gpu)

    image_files = [os.path.join(image_folder_path, f) for f in os.listdir(image_folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))]

    results_dict = process_images_in_batches(image_files, ocr, batch_size=batch_size)

    # 결과를 JSON 파일로 저장
    save_results_to_json(results_dict, output_json_path)

    print(f"OCR 결과가 {output_json_path}에 저장되었습니다.")
