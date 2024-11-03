import torch
import os
import json
from PIL import Image
from transformers import TrOCRProcessor, VisionEncoderDecoderModel, AutoTokenizer

# 모델과 프로세서 초기화
model_name = "team-lucid/trocr-small-korean"  # 모델 이름 정의
processor = TrOCRProcessor.from_pretrained(model_name)
model = VisionEncoderDecoderModel.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# 이미지 폴더 경로
image_folder_path = "../images_data/word"

# 결과 저장 폴더 확인 및 생성
output_folder = "predict_result"
os.makedirs(output_folder, exist_ok=True)  # exist_ok=True로 폴더가 없을 경우 생성

# JSON 결과를 저장할 파일 경로 설정
output_json_name = f"{model_name.split('/')[-1]}_result.json"
output_json_path = os.path.join(output_folder, output_json_name)

# 기존 결과 파일 로드 (재실행 시 중복 처리 방지)
if os.path.exists(output_json_path):
    with open(output_json_path, "r", encoding="utf-8") as json_file:
        results_dict = json.load(json_file)
else:
    results_dict = {}

# 이미지 파일 목록 생성
image_files = [os.path.join(image_folder_path, f) for f in os.listdir(image_folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))]

# 처리되지 않은 이미지 파일 필터링
processed_files = set(results_dict.keys())  # 이미 처리된 파일 이름 집합
unprocessed_files = [f for f in image_files if os.path.basename(f) not in processed_files]

# 각 이미지에 대해 OCR 수행
for idx, image_path in enumerate(unprocessed_files):
    # 이미지 열기
    image = Image.open(image_path).convert("RGB")  # 이미지 변환
    f_name = os.path.basename(image_path)  # 파일 이름 생성

    # 이미지로 OCR 수행
    pixel_values = processor(images=image, return_tensors="pt").pixel_values
    generated_ids = model.generate(pixel_values)
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

    # 결과를 딕셔너리에 저장
    results_dict[f_name] = generated_text  # 키: 파일 이름, 값: OCR 결과

    # 100개마다 중간 저장
    if (idx + 1) % 100 == 0 or (idx + 1) == len(unprocessed_files):  # 마지막에 도달한 경우도 포함
        with open(output_json_path, "w", encoding="utf-8") as json_file:
            json.dump(results_dict, json_file, ensure_ascii=False, indent=4)
        print(f"{idx + 1}/{len(unprocessed_files)} images processed and saved.")

print(f"최종 OCR 결과가 {output_json_path}에 저장되었습니다.")
