# main.py
from parsing import parse_input
# from food_prediction_test1 import find_closest_food
from food_prediction_test1 import find_top5_foods
from sklearn.metrics import accuracy_score

# OCR로부터 추출된 영양성분 (예시)
# input_nutrients_str = "탄수화물: 84g, 포화지방 9g, 당류: 2g, 단백질: 12g, 트랜스지방 0g"
# input_nutrients_str = "에너지: 478kcal, 단백질: 9.34g, 지방: 19.5g, 탄수화물: 66.2g, 당류: 4.58g, 나트륨: 594mg"
# input_nutrients_str = "에너지: 361kcal, 단백질: 9.28g, 지방: 10g, 탄수화물: 70.1g, 당류: 2g"

# 영양성분 파싱 (예시 문자열을 딕셔너리 형식으로 변환해야 함)
input_nutrients_86485 = {
    '에너지(kcal)': 177,
    '탄수화물(g)': 7.58,
    '나트륨(mg)' : 202.0,
    '당류(g)': 0.97,
    '지방(g)': 11.53,
    '트랜스지방산(g)' : 0.00,
    '포화지방산(g)' : 3.26, 
    '콜레스테롤(mg)' : 66.42,
    '단백질(g)': 10.72
}
# 식품코드 : 86485 / 식품명 : 맛나아바이순대 / 대식품명 : 순대 / 식품소분류명 : 즉석조리식품



# # 1. 입력값 전처리 (parsing.py 함수 호출)
# parsed_nutrients = parse_input(input_nutrients_str)

# # 2. 음식 예측 (food_prediction.py 함수 호출)
# predicted_food = find_closest_food(parsed_nutrients)

# print(f"가장 유사한 음식: {predicted_food}")


# 상위 5개의 음식 예측
top5_foods = find_top5_foods(input_nutrients_86485)
print("상위 5개의 예측된 음식:")
for i, food in enumerate(top5_foods, 1):
    print(f"{i}. {food}")
    
# 정확도 계산
def calculate_accuracy(test_data):
    correct = 0
    total = len(test_data)

    for input_nutrients, actual_food in test_data:
        predicted_foods = find_top5_foods(input_nutrients)  # 상위 5개의 예측 음식
        if actual_food in predicted_foods:
            correct += 1  # 상위 5개 중 하나라도 맞으면 correct 카운트 증가
    
    accuracy = correct / total
    return accuracy

# 테스트 데이터를 넣어 정확도 계산 (테스트 데이터는 input_nutrients와 실제 음식명을 쌍으로 만들어야 함)
test_data = [
    ({'탄수화물(g)': 84, '단백질(g)': 9.34, '지방(g)': 19.5, '에너지(kcal)': 478, '당류(g)': 4.58}, '예상 음식1'),
    ({'탄수화물(g)': 50, '단백질(g)': 8, '지방(g)': 15, '에너지(kcal)': 320, '당류(g)': 2}, '예상 음식2'),
    # 추가 테스트 케이스 작성 가능
]

accuracy = calculate_accuracy(test_data)
# print(f"정확도: {accuracy * 100:.2f}%")