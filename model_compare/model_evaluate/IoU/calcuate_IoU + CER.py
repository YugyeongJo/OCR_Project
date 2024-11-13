import json

def calculate_iou_from_corners(bbox1, bbox2):
    """
    두 바운딩 박스의 네 꼭짓점을 이용하여 IOU 계산.
    """
    bbox1_x_min = min(bbox1[0][0], bbox1[1][0], bbox1[2][0], bbox1[3][0])
    bbox1_x_max = max(bbox1[0][0], bbox1[1][0], bbox1[2][0], bbox1[3][0])
    bbox1_y_min = min(bbox1[0][1], bbox1[1][1], bbox1[2][1], bbox1[3][1])
    bbox1_y_max = max(bbox1[0][1], bbox1[1][1], bbox1[2][1], bbox1[3][1])

    bbox2_x_min = min(bbox2[0][0], bbox2[1][0], bbox2[2][0], bbox2[3][0])
    bbox2_x_max = max(bbox2[0][0], bbox2[1][0], bbox2[2][0], bbox2[3][0])
    bbox2_y_min = min(bbox2[0][1], bbox2[1][1], bbox2[2][1], bbox2[3][1])
    bbox2_y_max = max(bbox2[0][1], bbox2[1][1], bbox2[2][1], bbox2[3][1])

    intersection_x1 = max(bbox1_x_min, bbox2_x_min)
    intersection_y1 = max(bbox1_y_min, bbox2_y_min)
    intersection_x2 = min(bbox1_x_max, bbox2_x_max)
    intersection_y2 = min(bbox1_y_max, bbox2_y_max)

    intersection_width = max(0, intersection_x2 - intersection_x1)
    intersection_height = max(0, intersection_y2 - intersection_y1)
    intersection_area = intersection_width * intersection_height

    bbox1_area = (bbox1_x_max - bbox1_x_min) * (bbox1_y_max - bbox1_y_min)
    bbox2_area = (bbox2_x_max - bbox2_x_min) * (bbox2_y_max - bbox2_y_min)

    union_area = bbox1_area + bbox2_area - intersection_area
    iou = intersection_area / union_area if union_area > 0 else 0

    return iou

def parse_bbox_data(file_path):
    """
    주어진 파일에서 바운딩 박스 좌표만을 읽어와 리스트 형태로 반환.
    
    :param file_path: str, 텍스트 파일 경로
    :return: 리스트, 각 요소가 [(x1, y1), (x2, y2), (x3, y3), (x4, y4)] 형태의 바운딩 박스 좌표
    """
    result = []
    
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        coords = line.strip().split("##::")[0]
        coord_values = list(map(int, coords.split()))
        bbox = [
            (coord_values[0], coord_values[1]),
            (coord_values[2], coord_values[3]),
            (coord_values[4], coord_values[5]),
            (coord_values[6], coord_values[7])
        ]
        result.append(bbox)

    return result

def calculate_iou_for_files(target_data, compare_data):
    """
    두 파일의 바운딩 박스를 비교하여 각 바운딩 박스 쌍의 IOU를 계산하고 결과를 반환.
    
    :param target_data: str, 기준 데이터 파일 경로
    :param compare_data: str, 비교할 데이터 파일 경로
    :return: 딕셔너리, IOU 계산 결과
    """
    target_bboxes = parse_bbox_data(target_data)
    compare_bboxes = parse_bbox_data(compare_data)
    
    iou_results = []
    for t_index, t_bbox in enumerate(target_bboxes):  # target_bboxes 순회
        for c_index, c_bbox in enumerate(compare_bboxes):  # compare_bboxes 순회
            if t_index == c_index:
                iou = calculate_iou_from_corners(t_bbox, c_bbox)
                iou_results.append({
                    "target_index": t_index,
                    "compare_index": c_index,
                    "target_bbox": t_bbox,
                    "compare_bbox": c_bbox,
                    "iou": iou
            })
            # 디버깅 로그 추가
            print(f"Target {t_index} vs Compare {c_index}: IOU={iou}")
    
    return iou_results

if __name__ == "__main__":
    target_data = "C:/Users/dnltj/OneDrive/바탕 화면/iou_test/target/A_feeling_of_fried_onion_flavor_2.jpg.txt"
    compare_data = "C:/Users/dnltj/OneDrive/바탕 화면/iou_test/test/A_feeling_of_fried_onion_flavor_2.jpg.txt"
    
    # IOU 계산
    iou_results = calculate_iou_for_files(target_data, compare_data)

    # 결과 출력
    with open("iou_results.json", "w", encoding="utf-8") as f:
        json.dump(iou_results, f, indent=4, ensure_ascii=False)

    print("IOU 계산 결과가 iou_results.json에 저장되었습니다.")
