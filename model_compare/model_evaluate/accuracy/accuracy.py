import json
import os

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
        base_name, _ = os.path.splitext(file_name)  # 확장자 분리
        format_data[file_name] = pred_text  # 원래의 파일명을 키로 사용 (확장자를 포함)
    return format_data  # (예측값 출력 형식 요구사항: key는 이미지파일명.확장자, value는 pred data)

# 정확도 계산 함수
def calculate_accuracy(predicted_data, ground_truth_data):
    total_count = len(ground_truth_data)
    correct_count = sum(1 for image_name, gt_text in ground_truth_data.items()
                        if predicted_data.get(image_name, "") == gt_text)

    # 정확도 계산
    accuracy = (correct_count / total_count) * 100 if total_count > 0 else 0
    return accuracy

# 평가 및 정확도 출력
def evaluate_accuracy(predicted_file="ocr_result.json", ground_truth_file="ground_truth.json"):
    predicted_data, ground_truth_data = load_results(predicted_file, ground_truth_file)
    formatted_predictions = format_predictions(predicted_data)  # 예측값 형식화
    accuracy = calculate_accuracy(formatted_predictions, ground_truth_data)
    
    print(f"\nOCR 정확도: {accuracy:.2f}%")
    print("\n예측 결과:")
    #for image_name, pred_text in formatted_predictions.items():
        #print(f"{image_name}: {pred_text}")  # (예측값 출력 형식: 각 이미지 파일명과 예측 데이터 출력)

# 메인 실행
if __name__ == '__main__':
    print("================",os.getcwd())
    pred_path="daekeun_result.json"
    ground_path="ground_truth_20K.json"
    evaluate_accuracy(pred_path,ground_path)
