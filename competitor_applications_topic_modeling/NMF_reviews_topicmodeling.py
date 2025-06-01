from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
import pandas as pd
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import chardet
import random

# 사용자 정의 불용어
stop_words = [
    "사용", "좋아요", "편리", "도움이", "식단", "칼로리", "기록", "음식", "관리", "앱", 
    "매우", "최고", "그냥", "계속", "정말", "정말로", "너무", "다이어트", "있습니다", 
    "있습니다만", "개선", "필요", "확인", "부분", "가능", "활용", "등록", "사용중", 
    "설정", "사용자", "기능", "유용", "정보", "직접", "있습니다", "있다", "합니다", "합니다만",
    "이에요", "그리고", "또한", "너무나", "것", "하게", "때문에", "위해", "으로", "에서", 
    "그리고", "그", "수", "등", "또", "들", "다", "로", "의", "가", "이", "를", "을", 
    "과", "와", "는", "에", "한", "하여", "로서", "함", "하고", "할", "로", "임", "뿐", 
    "인", "에", "해서", "좀", "등", "대해", "위해", "거나", "때문", "하여", "도",
    "좋음", "괜찮음", "굿", "훌륭함", "추천", "강추", "만족", "좋다", "좋네요", "잘", "멋짐",
    "은", "요", "만", "편하고", "좋습니다", "안", "했는데", "같아요", "하는데", "보다", "입니다",
    "편해요", "좋겠습니다", "좋고", "^^","도움","하기"
]

# 강조할 키워드 목록
highlight_words = ["기록", "계산", "다이어트", "건강", "탄단지", "입력", "검색", "조절", "식단", "수정","추가","활기","회복","증진"]

# 파일 열기 및 인코딩 확인
with open('fat_secret_reviews.csv', 'rb') as f:
    result = chardet.detect(f.read())
    encoding = result['encoding']

# 감지된 인코딩으로 데이터 불러오기
df = pd.read_csv('fat_secret_reviews.csv', encoding="cp949")

# Okt 형태소 분석기 및 전처리 함수 정의
okt = Okt()

def preprocess(text):
    tokens = okt.morphs(text)
    tokens = [word for word in tokens if word not in stop_words]
    return ' '.join(tokens)

# content 컬럼 전처리
df['cleaned_content'] = df['content'].apply(preprocess)

# 모든 텍스트 결합
text = ' '.join(df['cleaned_content'])

highlight_words = ['불편', '오류', '느림', '버그', '수정','칼로리','사용','식단','다이어트','기록','음식','몸무게','어플','계산','검색','탄단지','체중'] 

# 색상 함수 정의
def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    if word in highlight_words:
        return "rgb(58, 204, 173)" 
    else:
        gray_value = random.randint(100, 200)
        return f"rgb({gray_value}, {gray_value}, {gray_value})"  

# 워드클라우드 객체 생성 및 텍스트 기반 생성
wordcloud = WordCloud(
    font_path='malgun.ttf',  
    width=800, 
    height=400, 
    background_color='white'
).generate(text) 

plt.figure(figsize=(10, 6))
plt.imshow(wordcloud.recolor(color_func=color_func), interpolation='bilinear')
plt.axis('off')  
plt.title("reviews Keywords")
plt.show()
