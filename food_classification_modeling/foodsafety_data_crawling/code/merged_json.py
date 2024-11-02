import json
import glob

# 합칠 JSON 파일들이 있는 경로 (예시: json_files 폴더에 있는 모든 .json 파일)
json_files = glob.glob("../data/*.json")

# 최종적으로 합칠 데이터를 저장할 딕셔너리
merged_data = {
    "prdlst_report_ledg_no": [],
    "manufacturer_name": [],
    "product_name": [],
    "report_number": [],
    "dosage_usage": [],
    "standards_specifications": []  # standards_specifications 추가
}

# 각 파일을 읽어서 데이터를 합치기
for file in json_files:
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        # 각 키에 데이터를 추가
        for key in merged_data.keys():
            if key in data:  # 해당 키가 데이터에 존재하는지 확인
                merged_data[key].extend(data[key])

# 합쳐진 데이터를 최종 JSON 파일로 저장
with open("merged_data.json", "w", encoding='utf-8') as f:
    json.dump(merged_data, f, ensure_ascii=False, indent=4)

print("모든 JSON 파일이 성공적으로 병합되었습니다!")
