import json

# 파일 경로 설정
ddobokki_result_path = "ddobokki_result.json"
ground_truth_path = "ground_truth.json"

# ddobokki_result.json 파일 로드
with open(ddobokki_result_path, "r", encoding="utf-8") as file:
    ddobokki_result = json.load(file)

# ground_truth.json 파일 로드
with open(ground_truth_path, "r", encoding="utf-8") as file:
    ground_truth = json.load(file)

# ddobokki_result.json의 키만 추출하여 ground_truth.json과 매칭
matched_data = {key: ground_truth[key] for key in ddobokki_result if key in ground_truth}

# 결과를 JSON 파일로 저장
with open("ground_truth_20K.json", "w", encoding="utf-8") as outfile:
    json.dump(matched_data, outfile, ensure_ascii=False, indent=4)

print("Matching complete. Results saved in matched_ground_truth.json")