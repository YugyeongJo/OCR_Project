def calculate_iou_from_corners(bbox1, bbox2):
    """
    두 바운딩 박스의 네 꼭짓점을 이용하여 IOU 계산.
    
    :param bbox1: 첫 번째 바운딩 박스의 네 꼭짓점 ((x1, y1), (x2, y2), (x3, y3), (x4, y4))
    :param bbox2: 두 번째 바운딩 박스의 네 꼭짓점 ((x1, y1), (x2, y2), (x3, y3), (x4, y4))
    :return: IOU (0과 1 사이)
    """
    # 각 바운딩 박스의 x, y 좌표 범위를 구합니다.
    bbox1_x_min = min(bbox1[0][0], bbox1[1][0], bbox1[2][0], bbox1[3][0])
    bbox1_x_max = max(bbox1[0][0], bbox1[1][0], bbox1[2][0], bbox1[3][0])
    bbox1_y_min = min(bbox1[0][1], bbox1[1][1], bbox1[2][1], bbox1[3][1])
    bbox1_y_max = max(bbox1[0][1], bbox1[1][1], bbox1[2][1], bbox1[3][1])

    bbox2_x_min = min(bbox2[0][0], bbox2[1][0], bbox2[2][0], bbox2[3][0])
    bbox2_x_max = max(bbox2[0][0], bbox2[1][0], bbox2[2][0], bbox2[3][0])
    bbox2_y_min = min(bbox2[0][1], bbox2[1][1], bbox2[2][1], bbox2[3][1])
    bbox2_y_max = max(bbox2[0][1], bbox2[1][1], bbox2[2][1], bbox2[3][1])

    # 교집합
    intersection_x1 = max(bbox1_x_min, bbox2_x_min)
    intersection_y1 = max(bbox1_y_min, bbox2_y_min)
    intersection_x2 = min(bbox1_x_max, bbox2_x_max)
    intersection_y2 = min(bbox1_y_max, bbox2_y_max)

    intersection_width = max(0, intersection_x2 - intersection_x1)
    intersection_height = max(0, intersection_y2 - intersection_y1)
    intersection_area = intersection_width * intersection_height

    # 각 바운딩 박스의 넓이 계산
    bbox1_area = (bbox1_x_max - bbox1_x_min) * (bbox1_y_max - bbox1_y_min)
    bbox2_area = (bbox2_x_max - bbox2_x_min) * (bbox2_y_max - bbox2_y_min)

    # IOU 계산
    union_area = bbox1_area + bbox2_area - intersection_area
    iou = intersection_area / union_area if union_area > 0 else 0

    return iou
