import jiwer
import json
import os

def calculate_wer_from_json(gt_file_path, pred_file_path, output_path):
    """
    Calculate WER between ground truth (GT) and prediction JSON dictionaries,
    and save the results in the specified JSON format.
    
    :param gt_file_path: Path to the ground truth JSON file
    :param pred_file_path: Path to the prediction JSON file
    :param output_path: Path to save the output JSON file
    :return: None
    """
    total_wer = 0
    count = 0
    predictions = {}

    # 단일 JSON 파일 비교
    with open(gt_file_path, 'r', encoding='utf-8') as gt_f, open(pred_file_path, 'r', encoding='utf-8') as pred_f:
        gt_data = json.load(gt_f)
        pred_data = json.load(pred_f)
        
        # 각 이미지 파일의 텍스트에 대해 WER 계산
        for key, gt_text in gt_data.items():
            pred_text = pred_data.get(key, "").strip()  # 예측 파일에서 해당 키의 텍스트를 가져옴
            
            # gt_text나 pred_text가 빈 문자열일 경우 건너뜁니다.
            if not gt_text.strip() or not pred_text:
                print(f"Skipping key '{key}' due to empty reference or hypothesis.")
                wer = 0.0
            else:
                wer = jiwer.wer(gt_text.strip(), pred_text)
                total_wer += wer
                count += 1

            # 각 키에 대한 WER을 predictions에 저장
            predictions[key] = wer
            print(f"WER for key '{key}': {wer:.4f}")

    # 평균 WER 계산
    avg_wer = total_wer / count if count > 0 else 0
    print(f"\nAverage WER: {avg_wer:.4f}")

    # JSON으로 저장할 데이터 구성
    output_data = {
        "average_wer": avg_wer,
        "predictions": predictions
    }

    # JSON 파일로 저장
    with open(output_path, 'w', encoding='utf-8') as out_f:
        json.dump(output_data, out_f, ensure_ascii=False, indent=4)

# 메인 실행
if __name__ == '__main__':
    gt_file_path = "C:/Users/user/Desktop/SeSAC_DATA_AI/Medium_Project/OCR_Project/model_compare/model_evaluate/ground_truth/ground_truth_20K.json"
    pred_file_path_ddobokki = "C:/Users/user/Desktop/SeSAC_DATA_AI/Medium_Project/OCR_Project/model_compare/ddobokki/results/ddobokki_result.json"
    pred_path_trocr_small = "C:/Users/user/Desktop/SeSAC_DATA_AI/Medium_Project/OCR_Project/model_compare/trocr-small-korean/predict_result/trocr-small-korean_result.json" # trocr_small
    pred_path_padle = "C:/Users/user/Desktop/SeSAC_DATA_AI/Medium_Project/OCR_Project/model_compare/paddleocr/result/paddle_result.json" # padle
    pred_path_daekeun = "C:/Users/user/Desktop/SeSAC_DATA_AI/Medium_Project/OCR_Project/model_compare/deakeun/daekeun_result.json"
    pytesseract_path = 'C:/Users/user/Desktop/SeSAC_DATA_AI/Medium_Project/OCR_Project/model_compare/pytesseract/predict_result/pytesseract_result_edit.json'

    output_path = "wer_results.json"
    calculate_wer_from_json(gt_file_path, pytesseract_path, output_path)
