import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation as LDA
from wordcloud import WordCloud
from konlpy.tag import Okt
from mecab import MeCab
import matplotlib.pyplot as plt
import plotly.express as px

# 한국어 형태소 분석기 초기화
okt = Okt()

# 1. 데이터 불러오기
data = pd.read_csv('reviews_keywords.csv')
data.head()

# 분석을 위한 content 열 추출
df_fatsafety_reviews = data["content"].astype(str)

# stopwords.txt 파일에서 불용어 불러오기
with open('stopwords.txt', 'r', encoding='utf-8') as f:
    stopwords = f.read().splitlines()

# 명사 추출 및 불용어 제거 함수
def Tokenizer_noun(raw, pos=["Noun"], stopword=stopwords):
    word_list = []
    for word, tag in okt.pos(raw, norm=True, stem=True):
        if len(word) > 1 and tag in pos and word not in stopword:
            if okt.pos(word)[0][1] in ["NNG"]:  # 일반 명사인지 확인
                word_list.append(word)
    return " ".join(word_list)

# 중복 명사 제거 함수
def noun_set(raw):
    noun_list = list(set(raw.split(' ')))
    return " ".join(noun_list)

# 명사 추출 및 중복 제거 적용
df_fatsafety_reviews = df_fatsafety_reviews.apply(Tokenizer_noun)
df_fatsafety_reviews = df_fatsafety_reviews.apply(noun_set)

# 처리된 리뷰 확인
print(df_fatsafety_reviews.head())

# 2. TfidfVectorizer로 텍스트 데이터 벡터화
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(df_fatsafety_reviews)

# 3. LDA를 통한 토픽 모델링
n_topics = 3  # 추출할 토픽 수
lda_model = LDA(n_components=n_topics, random_state=42)
lda_model.fit(tfidf_matrix)

# 4. LDA 결과 저장
topic_results = []
for index, topic in enumerate(lda_model.components_):
    topic_words = [tfidf_vectorizer.get_feature_names_out()[i] for i in topic.argsort()[-10:]]
    topic_results.append({
        "Topic": f"토픽 {index + 1}",
        "Top Words": ", ".join(topic_words)
    })

# 결과를 DataFrame으로 변환
topic_df = pd.DataFrame(topic_results)

# 결과를 CSV 파일로 저장
topic_df.to_csv('lda_topic_results.csv', index=False, encoding='utf-8-sig')

# 5. Plotly를 사용한 시각화
fig = px.bar(topic_df, 
              x='Top Words', 
              y='Topic',
              title='LDA Topic Modeling Results',
              labels={'Top Words': '상위 단어', 'Topic': '토픽'},
              text='Top Words',
              orientation='h')
fig.update_traces(textposition='auto')
fig.update_layout(yaxis=dict(title='토픽'), xaxis=dict(title='상위 단어'))
fig.write_html('lda_topic_results.html')  # HTML 파일로 저장

# 6. 각 토픽에 대한 워드 클라우드 생성
for index, topic in enumerate(lda_model.components_):
    plt.figure(figsize=(10, 5))
    wordcloud = WordCloud(font_path='path_to_your_korean_font.ttf',  # 한국어 글꼴 경로 지정
                          background_color='white').generate_from_frequencies(dict(zip(tfidf_vectorizer.get_feature_names_out(), topic)))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(f'토픽 {index + 1}')
    plt.show()
