import json
import unicodedata

def combine_jamo_in_json(input_path, output_path):
    """
    JSON 파일에서 분리된 한글 자모를 결합하여 원래 한글로 변환하고 결과를 새로운 JSON 파일에 저장합니다.
    
    :param input_path: 자모가 분리된 입력 JSON 파일 경로
    :param output_path: 결합된 한글을 저장할 출력 JSON 파일 경로
    """
    # JSON 파일 읽기
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 모든 문자열에서 자모를 결합
    combined_data = {key: unicodedata.normalize('NFC', value) for key, value in data.items()}
    
    # 결합된 데이터를 새로운 JSON 파일에 저장
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(combined_data, f, ensure_ascii=False, indent=4)
    
    print(f"Combined jamo JSON saved to {output_path}")

# 예시 실행
if __name__ == '__main__':
    input_path = "C:/Users/user/Desktop/SeSAC_DATA_AI/Medium_Project/OCR_Project/model_compare/ddobokki/results/ddobokki_result.json"
    output_path = "combined_ground_truth.json"
    combine_jamo_in_json(input_path, output_path)
