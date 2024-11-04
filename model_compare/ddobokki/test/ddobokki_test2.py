import os
import json
import torch
from transformers import TrOCRProcessor, VisionEncoderDecoderModel, AutoTokenizer
from io import BytesIO
from PIL import Image
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed

# 배치 및 병렬 처리를 위한 함수 정의
def process_batch(image_paths, model_name):
    device = "cpu"  # GPU가 없는 환경이므로 CPU 설정
    processor = TrOCRProcessor.from_pretrained(model_name)
    model = VisionEncoderDecoderModel.from_pretrained(model_name).to(device)

    results = []
    images = [Image.open(path).convert("RGB") for path in image_paths]
    pixel_values = processor(images=images, return_tensors="pt").pixel_values.to(device)  # padding 제거
    generated_ids = model.generate(pixel_values)
    generated_texts = processor.batch_decode(generated_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)  # 경고 제거
    for path, text in zip(image_paths, generated_texts):
        results.append((os.path.basename(path), text))
    return results

def save_intermediate_results(results, output_json_path):
    with open(output_json_path, "w+", encoding="utf-8") as json_file:
        json.dump(results, json_file, ensure_ascii=False, indent=4)

# 메인 블록
if __name__ == "__main__":
    model_name = "ddobokki/ko-trocr"
    image_folder_path = "C:/Users/eeooo/Desktop/OCR_Final/test_images"
    output_folder = "C:/Users/eeooo/Desktop/OCR_Final/predict_result_ddobokki"
    os.makedirs(output_folder, exist_ok=True)

    # JSON 결과를 저장할 딕셔너리 초기화
    results_dict = {}
    output_json_name = f"{model_name.split('/')[-1]}_result.json"
    output_json_path = os.path.join(output_folder, output_json_name)

    # 이미지 파일 목록 생성
    image_files = [os.path.join(image_folder_path, f) for f in os.listdir(image_folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
    batch_size = 16  # 배치 크기 설정
    num_workers = 4  # 병렬 프로세스 개수 설정 (CPU 코어 수에 따라 조정 가능)

    # tqdm 진행률 표시와 병렬 처리로 OCR 수행
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = []
        for i in range(0, len(image_files), batch_size):
            batch_files = image_files[i:i + batch_size]
            futures.append(executor.submit(process_batch, batch_files, model_name))

        # 병렬 처리된 결과 수집 및 저장
        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing images"):
            for f_name, generated_text in future.result():
                results_dict[f_name] = generated_text

            # 중간 결과를 저장 (중단 시 복구 가능)
            save_intermediate_results(results_dict, output_json_path)

    print(f"OCR 결과가 {output_json_path}에 저장되었습니다.")
