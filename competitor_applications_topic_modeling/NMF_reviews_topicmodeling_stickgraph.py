import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
from konlpy.tag import Okt
import platform

# 한글 폰트 설정
if platform.system() == "Darwin":  # macOS
    plt.rc("font", family="AppleGothic")
elif platform.system() == "Windows":  # Windows
    plt.rc("font", family="Malgun Gothic")
else:  # Linux (assuming Ubuntu)
    plt.rc("font", family="NanumGothic")

# CSV 파일 로드
file_path = 'fat_secret_reviews.csv'  # CSV 파일 경로를 지정하세요
words = ["기록", "계산", "다이어트", "건강", "탄단지", "입력", "검색", "조절", "식단", "수정", "추가", "활기", "회복", "증진"]

# 제외할 단어 목록
exclude_words = ["입니다", "있습니다", "합니다", "그", "그리고", "또한", "때문에", "위해", "수", "등", "이",
                ".","이","에","가","도","을",",", "좋아요","앱","할","의","를","으로","너무","하기","것","도움",
                "사용","음식","추가","잘","하고","들","하는","로","어플","은","한","때", "다이어트","!","해서","좋습니다",
                "안","많이","다","가능","는","요", "탄","단지","있어서","체중","?","적","같아요","..","조절","최고", "됩니다",
                "더","하면","만","내","비율","정말","중","제"]

# 데이터 불러오기
df = pd.read_csv(file_path, encoding="cp949")

# "content" 컬럼에서 특정 단어가 포함된 항목 추출
filtered_contents = df[df['content'].apply(lambda x: any(word in str(x) for word in words))]['content']

# 형태소 분석기
okt = Okt()

# 형태소 분석 및 단어 빈도수 계산
def preprocess_and_count(contents):
    tokens = []
    for content in contents:
        tokens.extend(okt.morphs(content))
    # 제외할 단어 필터링
    tokens = [token for token in tokens if token not in exclude_words]
    return Counter(tokens)

# 단어 빈도수 계산
word_counts = preprocess_and_count(filtered_contents)

# 상위 20개 단어 추출
sorted_word_counts = word_counts.most_common(20)
words, counts = zip(*sorted_word_counts)

# 막대그래프 생성
plt.figure(figsize=(12, 6))
bars = plt.bar(words, counts, alpha=0.8, color="skyblue")
plt.xlabel('단어', fontsize=12)
plt.ylabel('빈도수', fontsize=12)
plt.title('단어 빈도 비교', fontsize=15)
plt.xticks(rotation=45, fontsize=10)

# 각 막대 위에 빈도수 표시
for bar, count in zip(bars, counts):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height, str(count), ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.show()
