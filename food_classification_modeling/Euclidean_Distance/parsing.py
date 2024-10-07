# parsing.py
import re
from standard_columns import standard_columns  # standard_columns를 불러옴

def parse_input(input_data):
    """
    input_data는 딕셔너리 형식일 수도 있고, 문자열 형식일 수도 있습니다.
    문자열 형식으로 들어온 경우 영양소 이름과 값을 추출하여 표준 컬럼명과 매핑합니다.
    """
    parsed_data = {}
    
    if isinstance(input_data, dict):
        # 입력이 딕셔너리일 경우 처리
        for key, value in input_data.items():
            for nutrient, column in standard_columns.items():
                if nutrient in key:
                    parsed_data[column] = float(re.findall(r'\d+', str(value))[0])  # 숫자 추출
                    break
    
    elif isinstance(input_data, str):
        # 입력이 문자열일 경우 처리
        nutrients = input_data.split(',')
        for nutrient in nutrients:
            name_value = nutrient.split(':')
            if len(name_value) == 2:
                name, value = name_value[0].strip(), name_value[1].strip()
            else:
                name, value = nutrient.split()[0], nutrient.split()[1]
            
            for nutrient, column in standard_columns.items():
                if nutrient in name:
                    parsed_data[column] = float(re.findall(r'\d+', value)[0])  # 숫자 추출
                    break
    
    return parsed_data
