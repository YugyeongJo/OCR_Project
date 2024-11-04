import os
import torch
import json
from transformers import TrOCRProcessor, VisionEncoderDecoderModel, AutoTokenizer
from io import BytesIO
from PIL import Image
from tqdm import tqdm

def initialize_model(model_name, device):
    """모델과 프로세서를 초기화하는 함수"""
    processor = TrOCRProcessor.from_pretrained(model_name)
    model = VisionEncoderDecoderModel.from_pretrained(model_name).to(device)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    return processor, model, tokenizer

def process_images_in_batches(image_files, batch_size, processor, model, device):
    """이미지 파일을 배치로 처리하고 결과를 반환하는 함수"""
    results_dict = {}
    
    for i in tqdm(range(0, len(image_files), batch_size), desc="Processing images"):
        batch_files = image_files[i:i + batch_size]
        images = [Image.open(file).convert("RGB") for file in batch_files]
        pixel_values = processor(images=images, return_tensors="pt").pixel_values.to(device)  # padding 제거
        generated_ids = model.generate(pixel_values)
        generated_texts = processor.batch_decode(generated_ids, skip_special_tokens=True)

        for f_name, text in zip([os.path.basename(f) for f in batch_files], generated_texts):
            results_dict[f_name] = text
    
    return results_dict

def save_results_to_json(results_dict, output_path):
    """결과를 JSON 파일로 저장하는 함수"""
    with open(output_path, "w+", encoding="utf-8") as json_file:
        json.dump(results_dict, json_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    # 설정
    model_name = "ddobokki/ko-trocr"
    batch_size = 16  # 배치 크기 설정
    image_folder_path = "C:/Users/eeooo/Desktop/OCR_Final/test_images"
    output_folder = "C:/Users/eeooo/Desktop/OCR_Final/predict_result_ddobokki"
    os.makedirs(output_folder, exist_ok=True)
    output_json_name = f"{model_name.split('/')[-1]}_result.json"
    output_json_path = os.path.join(output_folder, output_json_name)

    # GPU 사용 가능 여부 확인
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    # 모델과 프로세서 초기화
    processor, model, tokenizer = initialize_model(model_name, device)

    # 이미지 파일 목록 생성
    image_files = [os.path.join(image_folder_path, f) for f in os.listdir(image_folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))]

    # 배치 처리로 OCR 수행
    results_dict = process_images_in_batches(image_files, batch_size, processor, model, device)

    # 결과를 JSON 파일로 저장
    save_results_to_json(results_dict, output_json_path)

    print(f"OCR 결과가 {output_json_path}에 저장되었습니다.")
