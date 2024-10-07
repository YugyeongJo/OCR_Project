# food_prediction.py
import numpy as np
import pandas as pd

# CSV 파일 로드
# file_path = 'data/11_영양소파일.csv'  # 경로는 맞게 수정하세요
file_path = 'data/14_영양성분_9개.csv'
nutrient_data = pd.read_csv(file_path)

# 필요한 열(탄수화물, 단백질, 지방 등)을 추출합니다.
nutrient_cols = [
    '에너지(kcal)', 
    '탄수화물(g)', 
    '나트륨(mg)', 
    '당류(g)', 
    '지방(g)', 
    '트랜스지방산(g)', 
    '포화지방산(g)', 
    '콜레스테롤(mg)',
    '단백질(g)']  # 필요한 영양소 항목 추가
nutrient_data_filtered = nutrient_data[['식품명'] + nutrient_cols].dropna()

def find_top5_foods(input_nutrients):
    """
    input_nutrients: 딕셔너리 형식으로 영양성분 값이 입력됩니다. {'탄수화물(g)': 84, '단백질(g)': 12, '지방(g)': 9}
    """
    input_array = np.array([input_nutrients.get(col, 0) for col in nutrient_cols])
    
    # 데이터베이스에서 각 음식의 영양소를 배열로 변환
    food_arrays = nutrient_data_filtered[nutrient_cols].to_numpy()
    
    # 유클리드 거리 계산 (입력값과 각 음식의 영양성분 간 차이 계산)
    distances = np.linalg.norm(food_arrays - input_array, axis=1)
    
    # 상위 5개의 음식 찾기
    top5_idx = np.argsort(distances)[:5]
    top5_foods = nutrient_data_filtered.iloc[top5_idx]['식품명'].tolist()  # 리스트로 변환
    
    return top5_foods


def find_closest_food(input_nutrients):
    """
    input_nutrients: 딕셔너리 형식으로 영양성분 값이 입력됩니다. {'탄수화물(g)': 84, '단백질(g)': 12, '지방(g)': 9}
    """
    input_array = np.array([input_nutrients.get(col, 0) for col in nutrient_cols])
    
    # 데이터베이스에서 각 음식의 영양소를 배열로 변환
    food_arrays = nutrient_data_filtered[nutrient_cols].to_numpy()
    
    # 유클리드 거리 계산 (입력값과 각 음식의 영양성분 간 차이 계산)
    distances = np.linalg.norm(food_arrays - input_array, axis=1)
    
    # 가장 유사한 음식 찾기
    closest_idx = np.argmin(distances)
    closest_food = nutrient_data_filtered.iloc[closest_idx]['식품명']
    
    return closest_food
