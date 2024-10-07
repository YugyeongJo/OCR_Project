### 한글 폰트 설치
!apt-get install -y fonts-nanum
!fc-cache -fv
!rm ~/.cache/matplotlib -rf
# 설치 후 colab의 경우 Runtime > Restart session 필요


import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rc('font', family='NanumBarunGothic') # 혹은 다른 설치한 Nanum 폰트 사용

import pandas as pd
import seaborn as sns
import numpy as np
import scipy
import scipy.stats as stats
import re
from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
import pyLDAvis
import pyLDAvis.lda_model
from sklearn.decomposition import LatentDirichletAllocation

# 형태소 분석기 인스턴스 생성
okt = Okt()

def tokenizer(raw, pos=["None", "Adverb", "Verb"], stopword = stopwords):
    return[
        word for word, tag in okt.pos(
            raw, 
            norm = True, 
            stem = True
        )
        if len(word) > 1 and tag in pos and word not in stopword
    ]
    
# tokenizer
tfidfVectorizer = TfidfVectorizer(tokenizer=tokenizer, max_df=0.85, min_df=2)