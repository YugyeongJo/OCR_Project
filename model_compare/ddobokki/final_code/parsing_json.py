import json

# 정답지 JSON 파일 경로
answer_file_path = "printed_data_info.json"

# JSON 파일 로드
with open(answer_file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# 파싱한 데이터를 저장할 딕셔너리 생성
parsed_data = {}

# 이미지 ID와 파일명을 매핑하는 딕셔너리 생성
file_name_map = {image["id"]: image["file_name"] for image in data["images"]}

# annotations에서 image_id와 text를 추출하고 file_name_map을 사용하여 file_name을 찾음
for annotation in data["annotations"]:
    image_id = annotation["image_id"]
    text = annotation["text"]
    
    # 이미지 ID에 해당하는 파일 이름을 가져옴
    file_name = file_name_map.get(image_id)
    if file_name:
        # 파일 이름을 key로 하고, text를 value로 저장
        parsed_data[file_name] = text


# 결과를 JSON 파일로 저장
with open("ground_truth.json", "w", encoding="utf-8") as outfile:
    json.dump(parsed_data, outfile, ensure_ascii=False, indent=4)

print("Parsing complete. Results saved in ground_truth.json")