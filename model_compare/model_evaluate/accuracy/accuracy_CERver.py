import json
import os
from jamo import h2j, j2hcj  # 자모 분리 라이브러리

# OCR 결과와 정답 데이터를 불러오는 함수
def load_results(predicted_file="daekeun_result.json", ground_truth_file="ground_truth_20K.json"):
    try:
        with open(predicted_file, 'r', encoding='utf-8') as pred_file:
            predicted_data = json.load(pred_file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading predicted file: {e}")
        return {}, {}
    
    try:
        with open(ground_truth_file, 'r', encoding='utf-8') as gt_file:
            ground_truth_data = json.load(gt_file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading ground truth file: {e}")
        return {}, {}
    
    return predicted_data, ground_truth_data

# 예측 결과를 딕셔너리 형태로 변환하는 함수
def format_predictions(predicted_data):
    format_data = {}
    for file_name, pred_text in predicted_data.items():
        # 파일명에서 확장자를 분리
        base_name, _ = os.path.splitext(file_name)
        format_data[file_name] = pred_text  # 원래의 파일명을 키로 사용 (확장자를 포함)
    return format_data

# 개별 이미지 정확도 계산 함수 (자모 분리하여 비교)
def calculate_individual_accuracies(predicted_data, ground_truth_data):
    accuracies = {}
    for image_name, gt_text in ground_truth_data.items():
        pred_text = predicted_data.get(image_name, "")
        
        # 자모 분리하여 비교
        gt_text_normalized = j2hcj(h2j(gt_text))
        pred_text_normalized = j2hcj(h2j(pred_text))
        
        # 이미지 별 정확도: 자모 단위로 일치하면 100%, 아니면 0%
        accuracy = 100.0 if pred_text_normalized == gt_text_normalized else 0.0
        accuracies[image_name] = accuracy
    
    return accuracies

# 평가 및 정확도 출력
def evaluate_accuracy(predicted_file, ground_truth_file):
    predicted_data, ground_truth_data = load_results(predicted_file, ground_truth_file)
    formatted_predictions = format_predictions(predicted_data)  # 예측값 형식화
    individual_accuracies = calculate_individual_accuracies(formatted_predictions, ground_truth_data)

    average_accuracy = sum(individual_accuracies.values()) / len(individual_accuracies) if individual_accuracies else 0
    
    # 결과 JSON 저장
    result_data = {
        "accuracy": average_accuracy,
        "predictions": individual_accuracies    # 개별 이미지 정확도 저장
    }

    # 결과를 JSON 파일로 저장
    with open("accuracy_results.json", "w", encoding="utf-8") as outfile:
        json.dump(result_data, outfile, ensure_ascii=False, indent=4)
    
    print(f"\nOCR 정확도: {average_accuracy:.2f}%")
    print("Accuracy results saved in accuracy_results.json")

# 메인 실행
if __name__ == '__main__':
    pred_path="C:/Users/user/Desktop/SeSAC_DATA_AI/Medium_Project/OCR_Project/model_compare/ddobokki/results/ddobokki_result.json"
    ground_path="C:/Users/user/Desktop/SeSAC_DATA_AI/Medium_Project/OCR_Project/model_compare/model_evaluate/ground_truth/ground_truth_20K.json"
    evaluate_accuracy(pred_path, ground_path)
