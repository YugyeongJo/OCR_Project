import os
import json
import base64
from dotenv import load_dotenv
from datetime import datetime
from openai import OpenAI
from debugger import debug_shell

# .env 파일의 내용을 로드합니다.
load_dotenv()

# 환경 변수 가져오기
openai_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key = openai_api_key)

# 이미지 파일을 base64로 인코딩하는 함수
def encode_image(image_path):
    print(image_path)
    """이미지 파일을 base64로 인코딩하여 반환."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def get_nutrition_info_from_api(base64_image):
    """OpenAI API에 요청을 보내 영양 성분 정보를 가져온다."""
    # nutrition_info = json.dumps({
    #                     "칼로리": "59kcal",
    #                     "나트륨": "600mg",
    #                     "탄수화물": "40g",
    #                     "당류": "12g",
    #                     "지방": "18g",
    #                     "트랜스지방": "0g",
    #                     "포화지방": "33g",
    #                     "콜레스테롤": "40mg",
    #                     "단백질": "12g",
    #                     "비타민A": "117mg",
    #                     "나이아신": "3.78mgNE",
    #                     "아연": '1.57mg'
    #                 }, ensure_ascii=False)
    nutrition_info = json.dumps({
        "나트륨": "50",
        "탄수화물": "5",
        "당류": "5",
        "트렌스지방": "0",
        "포화지방": "0.6"
    }, ensure_ascii=False)
    print(nutrition_info)
    client = OpenAI(api_key=openai_api_key)
    example_image = encode_image("C:/Users/user/Desktop/images/2_low_fat_milk_1.jpg")
    # print(example_image)
    response = client.chat.completions.create(
        model="gpt-4o-mini",

        messages=[
            {
                "role": "system",
                "content": "You are able to read an image and extract nutritional information very precisely."},
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "what is in this images?"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url":  f"data:image/jpeg;base64,{example_image}"
                        }
                    }
                ]
            },
            {
                "role": "assistant", 
                "content": "test", 
            },
            {
                "role": "user", 
                "content": [
                    {
                        "type": "text",
                        "text": "what is in this images?"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ], 
            }
        ], 
        response_format = {
            "type": "json_schema",
            "json_schema": {
                "name": "nutrition_information",
                "schema": {
                    "type": "object",
                    "properties": {
                        "image_info": {
                            "type": "object",
                            "properties": {
                                "id": {
                                    "description": "이미지의 고유 식별자",
                                    "type": "string"
                                },
                                "width": {
                                    "description": "이미지의 가로 크기 (픽셀 단위)",
                                    "type": "integer"
                                },
                                "height": {
                                    "description": "이미지의 세로 크기 (픽셀 단위)",
                                    "type": "integer"
                                },
                                "file_name": {
                                    "description": "이미지 파일 이름",
                                    "type": "string"
                                },
                                "date_captured": {
                                    "description": "이미지 캡처 일시 [YYYY-MM-DD HH:MM:SS]",
                                    "type": "string"
                                }
                            },
                            "required": ["id", "width", "height", "file_name", "date_captured"]
                        },
                        "nutrition_info": {
                            "type": "object",
                            "properties": {
                                "탄수화물": {
                                    "description": "탄수화물의 양과 일일 기준치 비율",
                                    "type": "string"
                                },
                                "당류": {
                                    "description": "당류의 양과 일일 기준치 비율",
                                    "type": "string"
                                },
                                "지방": {
                                    "description": "지방의 양과 일일 기준치 비율",
                                    "type": "string"
                                },
                                "트렌스지방": {
                                    "description": "트렌스지방의 양",
                                    "type": "string"
                                },
                                "포화지방": {
                                    "description": "포화지방의 양과 일일 기준치 비율",
                                    "type": "string"
                                },
                                "콜레스테롤": {
                                    "description": "콜레스테롤의 양",
                                    "type": "string"
                                },
                                "나트륨": {
                                    "description": "나트륨의 양과 일일 기준치 비율",
                                    "type": "string"
                                },
                                "단백질": {
                                    "description": "단백질의 양과 일일 기준치 비율",
                                    "type": "string"
                                },
                                "칼로리": {
                                    "description": "총 칼로리",
                                    "type": "string"
                                }
                            },
                            "required": ["탄수화물", "당류", "지방", "트렌스지방", "포화지방", "콜레스테롤", "나트륨", "단백질", "칼로리"]
                        }
                    },
                    "required": ["image_info", "nutrition_info"]
                }
            }
        },
    )
    print(response.choices[0].message.content)
    # debug_shell()
    return json.loads(response.choices[0].message.content)

def create_json_data(file_name, nutrition_info):
    """이미지 정보와 영양 성분 정보를 포함한 JSON 데이터를 생성."""
    json_data = {
        "image_info": {
            "id": os.path.splitext(file_name)[0],
            "width": 600,  
            "height": 314,
            "file_name": file_name,
            "date_captured": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        "nutrition_info": nutrition_info
    }
    return json_data

def save_json_data(json_data, output_path):
    """JSON 데이터를 파일로 저장."""
    with open(output_path, 'w+', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=4)
    print(f"Saved JSON at {output_path}")

def process_images_in_folder(folder_path, output_folder):
    """폴더 내 이미지를 처리하고 영양 성분 JSON 파일을 생성."""
    for file_name in os.listdir(folder_path):
        image_path = os.path.join(folder_path, file_name)
        
        if image_path.lower().endswith(('.jpg', '.jpeg', '.png')):
            base64_image = encode_image(image_path)
            nutrition_info = get_nutrition_info_from_api(base64_image)
            print(image_path)
            json_data = create_json_data(file_name, nutrition_info)
            
            output_path = os.path.join(output_folder, f"{os.path.splitext(file_name)[0]}.json")
            save_json_data(json_data, output_path)

# 실행 코드 예시
if __name__ == "__main__":
    # 이미지가 있는 폴더 경로와 JSON 파일이 저장될 출력 폴더 경로 설정
    folder_path = "C:/Users/user/Desktop/images"  # 이미지 폴더 경로를 입력하세요
    output_folder = "C:/Users/user/Desktop/json_file"  # JSON 파일을 저장할 폴더 경로를 입력하세요

    # 출력 폴더가 없는 경우 생성
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 이미지 처리 함수 호출
    process_images_in_folder(folder_path, output_folder)
