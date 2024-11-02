from transformers import TrOCRProcessor, VisionEncoderDecoderModel, AutoTokenizer
from PIL import Image
import requests
from io import BytesIO
import json
import os

# TrOCR 설정
processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
model = VisionEncoderDecoderModel.from_pretrained("daekeun-ml/ko-trocr-base-nsmc-news-chatbot")
tokenizer = AutoTokenizer.from_pretrained("daekeun-ml/ko-trocr-base-nsmc-news-chatbot")

# JSON 파일로 저장
def save_json(data, filename="ocr_result.json"):
    with open(os.path.join(os.getcwd(), filename), 'w+', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)

# TrOCR로 텍스트 감지 함수 정의
def detect_text(image_path):
    # 이미지 열기
    image = Image.open(image_path).convert("RGB")
    
    # TrOCR 텍스트 감지
    pixel_values = processor(image, return_tensors="pt").pixel_values
    generated_ids = model.generate(pixel_values, max_length=64)
    trocr_text = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

    print(f"Detected text for {image_path}: {trocr_text}") # 디버그 출력

    return trocr_text

# 폴더 혹은 이미지 단일 파일에 대한 OCR 실행 및 결과 저장
def process_images(path):
    result_dict = {}

    # 폴더 내 이미지 처리
    if os.path.isdir(path):
        img_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        for img_file in img_files:
            img_path = os.path.join(path, img_file)
            result_dict[img_file] = detect_text(img_path)
    else:
        result_dict[os.path.basename(path)] = detect_text(path)

    # 결과 저장
    save_json(result_dict)

# 메인 실행
if __name__ == '__main__':
    path = 'H:/image_or_folder'  # 이미지가 있는 폴더 또는 이미지 파일 경로
    process_images(path)
