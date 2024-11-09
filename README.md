# OCR Project 📷

> **TrOCR 모델과 CRAFT 모델을 활용한 식품 영양성분표 텍스트 추출 시스템**

## 📝 Description 
이 프로젝트는 TrOCR(Transformer-based Optical Character Recognition)와 CRAFT(Character Region Awareness for Text detection) 모델을 결합하여 식품 영양성분표 이미지에서 텍스트를 정확하게 추출합니다. 추출된 텍스트를 바탕으로 개인 맞춤형 식단 관리 서비스에 이용할 수 있습니다. 

- **주요 목표**: 사용자가 제공한 식품 이미지로부터 텍스트를 자동으로 인식하고 이를 맞춤형 영양 성분 데이터로 활용
- **기술 요약**: CRAFT 모델로 텍스트 영역을 감지하고, TrOCR 모델로 인식된 텍스트를 추출

## 🏗️ Model Architecture
### CRAFT (Character Region Awareness for Text Detection)
CRAFT 모델은 이미지에서 문자 영역을 감지하는 데 사용됩니다. 이 모델은 다음과 같은 방식으로 작동합니다:
- **Input**: 식품 영양성분표 이미지
- **Processing**: 이미지의 문자 영역을 탐지하여 각 영역의 위치 정보를 제공합니다. 
- **Output**: 탐지된 문자 영역의 바운딩 박스 (bounding boxes).

### TrOCR (Transformer-based Optical Character Recognition)
TrOCR 모델은 CRAFT 모델이 제공한 바운딩 박스를 기반으로 텍스트를 인식하는 데 사용됩니다. 작동 방식은 다음과 같습니다:
- **Input**: CRAFT로부터 전달받은 바운딩 박스의 이미지
- **Processing**: Transformer 아키텍처를 이용하여 텍스트를 추출합니다. 이 과정에서 모델은 자연어 처리 기술을 적용하여 의미 있는 텍스트를 생성합니다.
- **Output**: 추출된 텍스트 데이터.

## 🛠 Stack
- Python 3.8+
- CRAFT for text detection
- TrOCR for text recognition
- PyTorch for deep learning modeling
- OpenCV for image processing

|<center>PyTorch</center>|<center>HuggingFace</center>|
|--|--|
|<p align="center"><img alt="Pytorch" src="./icons/PyTorch-Dark.svg" width="48"></p>||
|<img src="https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white">|<img src="https://img.shields.io/badge/HuggingFace-%23FFBF00.svg?style=for-the-badge&logo=huggingface&logoColor=black">|

## 📊 Dataset
- **데이터 출처**: 식품 영양성분표 이미지 (사용자가 업로드한 사진)
- **데이터 형식**: JPEG, PNG 이미지 파일
- **용도**: OCR 텍스트 추출 및 분석에 활용

## 🚀 Installation
```bash
# Install dependencies
pip install -r requirements.txt

# 환경변수 설정 (예: Tesseract 경로 설정)
export TESSDATA_PREFIX=/path/to/tesseract/
```

## Usage
```bash
from scripts.ocr import ocr_extract, text_summarize

# 이미지에서 텍스트 추출
extracted_text = ocr_extract("sample_image.jpg")

# 텍스트 요약 및 분석
summary = text_summarize(extracted_text)
print("요약된 영양 성분 정보:", summary)
```

## 📁 Directory Structure

```markdown
OCR_Project/
├── data/                   # 샘플 이미지 데이터 및 데이터셋
├── model/                  # 학습된 모델 파일 (CRAFT, TrOCR 등)
├── scripts/                # OCR 추출 및 분석 코드
├── utils/                  # 데이터 전처리 및 텍스트 후처리 함수
├── competitor_applications_topic_modeling/  # 벤치마킹 분석 폴더 (optional)
├── food_classification_modeling/  # 식품 분류 모델링 코드
├── study_file/             # 프로젝트 관련 학습 및 연구 자료
└── README.md               # 프로젝트 설명 파일
```

## 👥 Team Members
|이름|역할|Github|
|--|--|--|
|**문상흠**|||
|**박창현**|||
|**이동준**|||
|**위서현**|||
|**조유경**||https://github.com/YugyeongJo|
|**한동우**|||
