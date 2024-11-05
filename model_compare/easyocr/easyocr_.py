import easyocr
import os
import sys
import numpy as np
import json
from PIL import Image

sys.path.append(os.path.abspath('..'))
from model_evaluate.accuracy import accuracy
from model_compare.ddobokki.test import CER_jamo_final_test1
from model_evaluate.WER import wer

def parse_str(array):
    output = ''
    for lst in array:
        for item in lst:
            if type(item) == str:
                output = item
                return output
            
    
def result_easyocr(folder_path):
    folder_path = folder_path
    image_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(('.png'))]

    # 결과 저장 폴더 확인 및 생성
    output_folder = "predict_result"
    os.makedirs(output_folder, exist_ok=True)  # exist_ok=True로 폴더가 없을 경우 생성

    # JSON 결과를 저장할 딕셔너리 초기화
    results_dict = {}

    # 각 이미지에 대해 OCR 수행
    for idx, image_path in enumerate(image_files):
        
        # 이미지 열기
        image = Image.open(image_path)
        f_name = os.path.basename(image_path)
        
        org_image = np.asarray(image)

        # EasyOCR 리더 초기화 (한국어와 영어 설정)
        reader = easyocr.Reader(lang_list = ['ko', 'en'], gpu = True)
        
        # 전처리 없이 바로 이미지에서 OCR 수행
        results = reader.readtext(org_image)
        result = parse_str(results)

        results_dict[f_name] = result
        
        
        print(idx)

    model_name = 'easyOCR'
    output_json_name = f"{model_name}_result.json"  # 모델 이름을 포함한 JSON 파일 이름 생성
    output_json_path = os.path.join(output_folder, output_json_name)
    with open(output_json_path, "w+", encoding="utf-8") as json_file:
        json.dump(results_dict, json_file, ensure_ascii = False, indent = 4)  # JSON 파일 저장

    print(f"OCR 결과가 {output_json_path}에 저장되었습니다.")

if __name__ == '__main__':
    easyocr_json = 'C:/OCR_Project/model_compare/easyocr/predict_result/easyOCR_result.json'
    ground_json = 'C:/OCR_Project/model_compare/model_evaluate/ground_truth/ground_truth.json'
    output_path = 'C:/OCR_Project/model_compare/easyocr/predict_result'
    accuracy.evaluate_accuracy(easyocr_json, ground_json)
    CER_jamo_final_test1.calculate_cer(easyocr_json, ground_json, output_path)
    wer.calculate_wer_from_json(ground_json, easyocr_json, output_path)