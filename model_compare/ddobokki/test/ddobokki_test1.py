import os
import torch
import json
from transformers import pipeline
from transformers import AutoTokenizer, AutoModel
from transformers import TrOCRProcessor, VisionEncoderDecoderModel, AutoTokenizer
from io import BytesIO
from PIL import Image
from tqdm import tqdm

# GPU 사용 가능 여부 확인
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# 모델과 프로세서 초기화
model_name = "ddobokki/ko-trocr"  # 모델 이름 정의
processor = TrOCRProcessor.from_pretrained(model_name)
model = VisionEncoderDecoderModel.from_pretrained(model_name).to(device)
tokenizer = AutoTokenizer.from_pretrained(model_name)

image_folder_path = "C:/Users/eeooo/Desktop/OCR_Final/test_images"

# 결과 저장 폴더 확인 및 생성
output_folder = "C:/Users/eeooo/Desktop/OCR_Final/predict_result_ddobokki"
os.makedirs(output_folder, exist_ok=True)  # exist_ok=True로 폴더가 없을 경우 생성

# JSON 결과를 저장할 딕셔너리 초기화
results_dict = {}

# 이미지 파일 목록 생성
image_files = [os.path.join(image_folder_path, f) for f in os.listdir(image_folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))]

    
# 각 이미지에 대해 OCR 수행
for image_path in tqdm(image_files, desc="Processing images"):
    # 이미지 열기
    image = Image.open(image_path).convert("RGB")  # 이미지 변환
    f_name = os.path.basename(image_path) # 파일 이름 생성
    
    # 이미지로 OCR 수행
    pixel_values = processor(images=image, return_tensors="pt").pixel_values.to(device)
    generated_ids = model.generate(pixel_values)
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    
    # 결과를 딕셔너리에 저장
    results_dict[f_name] = generated_text  # 키: 파일 이름, 값: OCR 결과
    
# 결과를 JSON 파일로 저장
output_json_name = f"{model_name.split('/')[-1]}_result.json"  # 모델 이름을 포함한 JSON 파일 이름 생성
output_json_path = os.path.join(output_folder, output_json_name)
with open(output_json_path, "w+", encoding="utf-8") as json_file:
    json.dump(results_dict, json_file, ensure_ascii=False, indent=4)  # JSON 파일 저장

print(f"OCR 결과가 {output_json_path}에 저장되었습니다.")