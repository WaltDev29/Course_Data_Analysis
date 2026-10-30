# 영화 리뷰에서 명사를 추출해 빈도 막대그래프와 워드클라우드를 그리는 텍스트 마이닝 예제
import pandas as pd  # 데이터 처리 라이브러리
import matplotlib.pyplot as plt  # 그래프 출력용 라이브러리
from wordcloud import WordCloud  # 워드클라우드 생성 라이브러리
import konlpy  # 한국어 형태소 분석 라이브러리(Java 필요)
from pathlib import Path  # 파일 경로 처리용
import os, sys  # 환경 변수 설정, 현재 파이썬 환경 위치 확인용

# conda 환경에 설치한 JDK(openjdk)를 사용하도록 지정한다
# (VS Code가 conda 환경을 활성화하지 않고 실행하면 PC에 깔린 예전 Java 8을 잡아 오류가 나기 때문)
conda_jdk = Path(sys.prefix) / 'Library' / 'lib' / 'jvm'
if conda_jdk.exists():
    os.environ['JAVA_HOME'] = str(conda_jdk)

# 이 파일의 위치를 기준으로 데이터 폴더를 찾는다(어느 폴더에서 실행해도 동작)
DATA_DIR = Path(__file__).resolve().parents[1] / 'data'

# (1) 데이터 준비
df = pd.read_csv(DATA_DIR / 'movie1_review.csv')  # 영화 리뷰 데이터 읽기(Review 컬럼에 리뷰 문장)
print(df)  # 데이터 확인

# (2) 형태소 분석기 정의
kkma = konlpy.tag.Kkma() # 형태소 분석기 꼬꼬마(Kkma)

# (3) 단어 데이터프레임 만들기
nouns = df['Review'].apply(kkma.nouns)  # 리뷰마다 명사만 뽑아 리스트로 저장
print(nouns)  # 리뷰별 명사 리스트 확인

nouns = nouns.explode()  # 리스트를 풀어 명사 하나당 한 행으로 만들기
print(nouns)  # 결과 확인

# (4) 전처리 실시
# 모시 -> 티모시, imax -> 아이맥스,...
nouns[nouns=='모시'] = '티모시'  # 형태소 분석기가 잘못 자른 단어를 바로잡기
nouns[nouns=='IMAX'] = '아이맥스'  # 영어 표기를 한글로 통일
nouns[nouns=='파트3'] = '3편'  # 같은 뜻의 단어로 통일

# 글자 수 2개 이상인 단어만 추출
df_word = pd.DataFrame({'word' : nouns})  # 명사를 word 컬럼으로 갖는 데이터프레임
df_word['count'] = df_word['word'].str.len()  # 단어의 글자 수
df_word = df_word.query('count >= 2')  # 한 글자 단어 제외
print(df_word)  # 결과 확인

# 단어 빈도수 집계 및 정렬
df_word = df_word.groupby('word', as_index = False)  # 같은 단어끼리 묶기
df_word = df_word.count().sort_values('count', ascending = False)  # 단어별 등장 횟수, 많은 순 정렬
print(df_word)  # 결과 확인

# 불필요한 단어 제거
del_idx = df_word.loc[df_word.word.isin(['영화', '편이', '영화관', '파트' ])].index  # 제거할 단어의 행 번호
df_word = df_word.drop(index=del_idx)  # 해당 행 삭제

# (5) 워드클라우드 작성
# 빈도수 상위 10개 단어
plt.rcParams['font.family'] ='Malgun Gothic'  # 한글 폰트 설정
plt.rcParams['axes.unicode_minus'] =False  # 마이너스 부호 깨짐 방지

df_top10 = df_word.iloc[:10,:].sort_values('count', ascending=True)  # 상위 10개(그래프에서 위쪽이 큰 값이 되도록 오름차순)
df_top10.plot.barh(x='word', y='count')  # 가로 막대그래프
plt.show()  # 그래프 화면에 출력

# 워드클라우드
dic_word = df_word.set_index('word').to_dict()['count']  # {단어: 빈도수} 형태의 딕셔너리
print(dic_word)  # 결과 확인

wc = WordCloud(random_state=123,  # 매번 같은 배치가 나오도록 고정
               font_path='c:/Windows/Fonts/malgun.ttf',  # 한글 폰트 파일
               width=400,  # 이미지 폭(pixel)
               height=400,  # 이미지 높이(pixel)
               background_color='white')  # 배경색

img_wordcloud = wc.generate_from_frequencies(dic_word) # 워드클라우드 → 이미지로

plt.figure(figsize = (10, 10)) # 크기 지정하기
plt.axis('off') # 축 없애기
plt.imshow(img_wordcloud) # 결과 보여주기
plt.show() # 결과를 화면에 출력

# (6) 클라우드의 모양과 글씨 색상 변경
import PIL  # 이미지 처리 라이브러리
import numpy as np  # 배열 처리 라이브러리

icon = PIL.Image.open(DATA_DIR / 'cloud.png').convert("RGBA")  # 구름 모양 이미지 읽기(투명도 포함)
img = PIL.Image.new(mode = 'RGBA', size=icon.size, color=(255, 255, 255))  # 같은 크기의 흰색 바탕 이미지
img.paste(icon, icon)  # 흰 바탕 위에 구름 모양 붙이기(투명한 부분은 흰색으로)
img = np.array(img)  # 워드클라우드 마스크로 쓰기 위해 배열로 변환

wc = WordCloud(random_state=123,  # 매번 같은 배치가 나오도록 고정
               font_path='c:/Windows/Fonts/malgun.ttf',  # 한글 폰트 파일
               width=400,  # 이미지 폭(pixel)
               height=400,  # 이미지 높이(pixel)
               background_color='white',  # 배경색
               mask=img,  # 흰색이 아닌 부분(구름 모양)에만 단어 배치
               colormap='inferno')  # 글자 색 팔레트

img_wordcloud = wc.generate_from_frequencies(dic_word) # 워드클라우드 → 이미지

plt.figure(figsize = (10, 10)) # 크기 지정하기
plt.axis('off') # 축 없애기
plt.imshow(img_wordcloud) # 결과 보여주기
plt.show() # 결과를 화면에 출력