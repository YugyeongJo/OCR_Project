import jiwer
import glob
import json
import os

def calculate_wer_from_json(gt_path, pred_path, output_path):
    """
    Calculate WER between ground truth (GT) and predicted (D) JSON files,
    and save the results in the specified JSON format.
    
    :param gt_path: Directory containing ground truth JSON files
    :param pred_path: Directory containing prediction JSON files
    :param output_path: Path to save the output JSON file
    :return: None
    """
    gt_files = sorted(glob.glob(os.path.join(gt_path, '*.json')))
    pred_files = sorted(glob.glob(os.path.join(pred_path, '*.json')))
    
    if len(gt_files) != len(pred_files):
        print("Warning: Number of GT files and prediction files are different.")
    
    total_wer = 0
    count = 0
    predictions = {}

    for gt_file, pred_file in zip(gt_files, pred_files):
        with open(gt_file, 'r', encoding='utf-8') as gt_f, open(pred_file, 'r', encoding='utf-8') as pred_f:
            gt_data = json.load(gt_f)
            pred_data = json.load(pred_f)
            
            # JSON 구조에 따라 텍스트를 추출합니다.
            gt_text = gt_data.get('text', '').strip()
            pred_text = pred_data.get('text', '').strip()
            
            wer = jiwer.wer(gt_text, pred_text)
            total_wer += wer
            count += 1

            # 파일 이름과 WER을 predictions에 저장
            file_name = os.path.basename(gt_file)
            predictions[file_name] = wer

            print(f"WER for {gt_file} and {pred_file}: {wer:.4f}")

    avg_wer = total_wer / count if count > 0 else 0
    print(f"\nAverage WER: {avg_wer:.4f}")

    # JSON으로 저장할 데이터 구성
    output_data = {
        "accuracy": avg_wer,
        "predictions": predictions
    }

    # JSON 파일로 저장
    with open(output_path, 'w', encoding='utf-8') as out_f:
        json.dump(output_data, out_f, ensure_ascii=False, indent=4)

# # Usage example
# gt_path = 'SeSac/target.json'  # target json 파일 경로
# pred_path = 'SeSac/target.json'  # pred json 파일 경로
# output_path = 'output.json'  # 결과 저장할 파일 경로
# calculate_wer_from_json(gt_path, pred_path, output_path)

# 메인 실행
if __name__ == '__main__':
    pred_path_ddobokki ="C:/Users/user/Desktop/SeSAC_DATA_AI/Medium_Project/OCR_Project/model_compare/ddobokki/results/ddobokki_result.json" # ddobokki
    pred_path_trocr_small = "C:/Users/user/Desktop/SeSAC_DATA_AI/Medium_Project/OCR_Project/model_compare/trocr-small-korean/predict_result/trocr-small-korean_result.json" # trocr_small
    pred_path_padle = "C:/Users/user/Desktop/SeSAC_DATA_AI/Medium_Project/OCR_Project/model_compare/paddleocr/result/paddle_result.json" # padle
    ground_path="C:/Users/user/Desktop/SeSAC_DATA_AI/Medium_Project/OCR_Project/model_compare/model_evaluate/ground_truth/ground_truth_20K.json"
    output_path = "wer_results.json"
    calculate_wer_from_json(ground_path, pred_path_ddobokki, output_path)