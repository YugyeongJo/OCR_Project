import json
import numpy as np
from jamo import h2j, j2hcj  # 자모 분리 라이브러리
from difflib import SequenceMatcher

def cer(reference, hypothesis):
    """한글 CER을 계산하는 함수. 자모 단위로 문장을 비교합니다."""
    ref = j2hcj(h2j(reference))
    hyp = j2hcj(h2j(hypothesis))
    
    # Levenshtein Distance 계산
    matcher = SequenceMatcher(None, ref, hyp)
    edits = sum([sum(triple[-2:]) for triple in matcher.get_opcodes() if triple[0] != 'equal'])
    
    # CER 계산
    cer_score = edits / max(len(ref), 1)
    return cer_score

def load_json(file_path):
    """JSON 파일을 로드하는 함수"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading JSON file {file_path}: {e}")
        return {}

def calculate_cer(ocr_result_path, ground_truth_path, output_path="cer_results.json"):
    """OCR 결과와 정답 데이터를 비교하여 CER을 계산하고 JSON으로 저장하는 함수"""
    ocr_results = load_json(ocr_result_path)
    reference_texts = load_json(ground_truth_path)
    
    # CER 계산 및 결과 저장
    cer_results = {}
    for filename, ocr_text in ocr_results.items():
        reference_text = reference_texts.get(filename, "")
        cer_score = cer(reference_text, ocr_text)
        cer_results[filename] = cer_score
        print(f"File: {filename}, OCR: {ocr_text}, Reference: {reference_text}, CER: {cer_score:.4f}")

    # 전체 CER 평균 계산
    average_cer = np.mean(list(cer_results.values()))
    print(f"Average CER: {average_cer:.4f}")

    # 결과 JSON 생성
    result_data = {
        "average_cer": average_cer,
        "cer_scores": cer_results
    }

    # 결과를 JSON 파일로 저장
    with open(output_path, "w", encoding="utf-8") as outfile:
        json.dump(result_data, outfile, ensure_ascii=False, indent=4)
    
    print(f"CER calculation complete. Results saved in {output_path}")

# 함수 호출 예시
if __name__ == '__main__':
    # 각 OCR 결과 파일과 ground_truth 파일 경로 설정
    ddobokki_result_path = 'C:/Users/user/Desktop/SeSAC_DATA_AI/Medium_Project/OCR_Project/model_compare/ddobokki/results/ddobokki_result.json'  # 실제 파일 경로 입력
    daekeun_result_path = 'C:/Users/user/Desktop/SeSAC_DATA_AI/Medium_Project/OCR_Project/model_compare/deakeun/daekeun_result.json'  # 실제 파일 경로 입력
    small_korean_result_path = 'C:/Users/user/Desktop/SeSAC_DATA_AI/Medium_Project/OCR_Project/model_compare/trocr-small-korean/predict_result/trocr-small-korean_result.json'
    padle_result_path = 'C:/Users/user/Desktop/SeSAC_DATA_AI/Medium_Project/OCR_Project/model_compare/paddleocr/result/paddle_result.json'
    ground_truth_path = 'C:/Users/user/Desktop/SeSAC_DATA_AI/Medium_Project/OCR_Project/model_compare/model_evaluate/ground_truth/ground_truth_20K.json'
    output_path = 'cer_results.json'
    # CER 계산 함수 호출
    calculate_cer(padle_result_path, ground_truth_path, output_path)
