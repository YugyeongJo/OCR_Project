import streamlit as st
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image, ImageEnhance, ImageFilter
import pandas as pd
import torch

# TrOCR 모델과 프로세서 불러오기
processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")

# Streamlit 화면 구성
st.title("🥗 식단 관리 OCR 대시보드")
st.write("이미지를 업로드하여 영양 성분을 추출하고 관리하세요.")

# 사이드바 메뉴 (모바일 친화적 인터페이스 제공)
with st.sidebar:
    st.header("📱 메뉴")
    option = st.radio("기능 선택", ("영양 성분 추출", "영양 성분 데이터"))

# 이미지 파일 업로드
if option == "영양 성분 추출":
    st.subheader("📤 이미지를 업로드하세요")
    uploaded_file = st.file_uploader("식품 영양성분표 이미지를 업로드하세요", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="업로드된 이미지", use_column_width=True)

        # OCR 수행
        st.write("🔍 텍스트를 추출하는 중입니다...")
        pixel_values = processor(images=image, return_tensors="pt").pixel_values
        generated_ids = model.generate(pixel_values)
        text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

        # 추출된 텍스트 표시
        st.subheader("📝 추출된 텍스트")
        st.write(text)

        # 텍스트 파싱하여 데이터프레임 생성
        lines = text.split("\n")
        data = {"항목": [], "값": []}
        for line in lines:
            parts = line.split()
            if len(parts) > 1:
                data["항목"].append(" ".join(parts[:-1]))
                data["값"].append(parts[-1])
        
        # 데이터프레임 변환 및 캐싱
        df = pd.DataFrame(data)
        st.session_state["extracted_data"] = df  # 세션 상태에 저장
        st.success("✅ 텍스트 추출 완료")

# 영양 성분 데이터 표시
if option == "영양 성분 데이터":
    if "extracted_data" in st.session_state:
        df = st.session_state["extracted_data"]

        # 데이터프레임 표시
        st.subheader("🥗 영양 성분표 데이터")
        st.dataframe(df)

        # 차트 시각화
        numeric_columns = df[pd.to_numeric(df["값"], errors="coerce").notnull()]
        st.subheader("📊 영양 성분 차트")
        st.bar_chart(numeric_columns.set_index("항목").astype(float))

    else:
        st.info("💡 먼저 영양 성분 추출을 수행하세요.")
