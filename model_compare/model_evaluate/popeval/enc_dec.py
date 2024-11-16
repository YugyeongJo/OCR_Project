import os
from charset_normalizer import from_path

def detect_encoding(file_path):
    """파일의 인코딩을 추정"""
    try:
        result = from_path(file_path).best()
        return result.encoding if result else None
    except Exception as e:
        print(f"Failed to detect encoding for {file_path}: {e}")
        return None

def convert_to_utf8(file_path, original_encoding):
    """파일을 UTF-8로 변환"""
    try:
        with open(file_path, "r", encoding=original_encoding) as f:
            content = f.read()
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Converted: {file_path}")
    except Exception as e:
        print(f"Failed to convert {file_path}: {e}")

def batch_convert_to_utf8(folder_path):
    """폴더 내 모든 텍스트 파일을 UTF-8로 변환"""
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path) and file_name.endswith(".txt"):
            original_encoding = detect_encoding(file_path)
            print(f"{file_path} \n detected encoding: {original_encoding}")
            if original_encoding and original_encoding.lower() != "utf-8":
                convert_to_utf8(file_path, original_encoding)
            else:
                print(f"Skipping {file_path}: Already UTF-8 or encoding not detected.")

# 폴더 경로 설정
folder_path = "H:/OCR_Project/data_labeling/img_labeling/3/pred"
batch_convert_to_utf8(folder_path)
