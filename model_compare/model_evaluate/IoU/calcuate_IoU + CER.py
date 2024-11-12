import numpy as np
from difflib import SequenceMatcher
import json

def calculate_iou_from_corners(bbox1, bbox2):
    """
    두 바운딩 박스의 네 꼭짓점을 이용하여 IOU 계산.
    """
    bbox1_x_min = min(bbox1[0][0], bbox1[1][0], bbox1[2][0], bbox1[3][0])
    bbox1_x_max = max(bbox1[0][0], bbox1[1][0], bbox1[2][0], bbox1[2][0], bbox1[3][0])
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

def calculate_cer(text1, text2):
    """
    CER (Character Error Rate) 계산.
    """
    matcher = SequenceMatcher(None, text1, text2)
    distance = matcher.distance()
    cer = distance / max(len(text1), len(text2)) if max(len(text1), len(text2)) > 0 else 0

    return cer

def calculate_metrics(image_text_data, output_file="results.json"):
    """
    여러 이미지 텍스트에 대한 CER을 계산하고, 평균 CER과 각 이미지별 CER을 JSON 파일로 저장.
    
    :param image_text_data: 딕셔너리, {이미지 파일명: (예상 텍스트, 실제 텍스트)}
    :param output_file: JSON 파일로 저장할 파일명
    :return: None
    """
    predictions = {}
    total_cer = 0.0

    for image_name, (pred_text, actual_text) in image_text_data.items():
        cer = calculate_cer(pred_text, actual_text)
        predictions[image_name] = cer
        total_cer += cer

    average_cer = total_cer / len(image_text_data) if len(image_text_data) > 0 else 0
    result = {
        "average_cer": average_cer,
        "predictions": predictions
    }

    # JSON 파일로 저장
    with open(output_file, "w") as file:
        json.dump(result, file, indent=4)

# 예시 데이터
image_text_data = {
    "02234400.png": ("predicted text example", "predicted text example"),
    "02234402.png": ("example prediction", "example prediction"),
    "02234404.png": ("hello world", "helo wrld"),
    # 더 많은 데이터 추가 가능
}

# 결과를 JSON 파일로 저장
calculate_metrics(image_text_data)
