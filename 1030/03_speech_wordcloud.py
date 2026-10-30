# 반기문 국회 연설문에서 명사를 추출해 워드클라우드를 그리는 실전 분석
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

df = pd.read_fwf(DATA_DIR / '반기문_국회_연설문.txt').iloc[:, 0]  # 연설문 텍스트 파일을 줄 단위로 읽어 첫 열만 사용
print(df.head())  # 앞 5줄 확인

kkma = konlpy.tag.Kkma()  # 형태소 분석기 꼬꼬마(Kkma)

nouns = df.apply(kkma.nouns)  # 문장마다 명사만 뽑아 리스트로 저장
nouns = nouns.explode()  # 리스트를 풀어 명사 하나당 한 행으로 만들기
print(nouns)  # 결과 확인

# 글자 수 2개 이상인 단어만 추출
df_word = pd.DataFrame({'word': nouns})  # 명사를 word 컬럼으로 갖는 데이터프레임
df_word['count'] = df_word['word'].str.len()  # 단어의 글자 수
df_word = df_word.query('count >= 2')  # 한 글자 단어 제외
print(df_word)  # 결과 확인

# 단어 빈도수 집계 및 정렬
df_word = df_word.groupby('word', as_index=False)  # 같은 단어끼리 묶기
df_word = df_word.count().sort_values('count', ascending=False)  # 단어별 등장 횟수, 많은 순 정렬
print(df_word.head(10))  # 상위 10개 단어 확인

dic_word = df_word.set_index('word').to_dict()['count']  # {단어: 빈도수} 형태의 딕셔너리
print(dic_word)  # 결과 확인

wc = WordCloud(random_state=123,  # 매번 같은 배치가 나오도록 고정
               font_path='c:/Windows/Fonts/malgun.ttf',  # 한글 폰트 파일
               width=400,  # 이미지 폭(pixel)
               height=400,  # 이미지 높이(pixel)
               background_color='white')  # 배경색
img_wordcloud = wc.generate_from_frequencies(dic_word)  # 워드클라우드 -> 이미지

plt.figure(figsize=(10, 10))  # 크기 지정하기
plt.axis('off')  # 축 없애기
plt.imshow(img_wordcloud)  # 결과 보여주기
plt.show()  # 결과를 화면에 출력