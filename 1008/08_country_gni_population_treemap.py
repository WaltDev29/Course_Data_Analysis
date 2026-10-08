# 국가별 GNI·인구 데이터로 트리맵을 그려 웹 브라우저에 표시하는 예제
import plotly.express as px  # plotly 간편 시각화 모듈
import webbrowser  # 웹 브라우저 열기용
import matplotlib.pyplot as plt  # 그래프 출력용 라이브러리
import pandas as pd  # 데이터 처리 라이브러리
from pathlib import Path  # 파일 경로 처리용

# 이 파일의 위치를 기준으로 데이터 폴더를 찾는다(어느 폴더에서 실행해도 동작)
DATA_DIR = Path(__file__).resolve().parents[2] / 'data'

df = pd.read_csv(DATA_DIR / 'GNI2014.csv')  # 2014년 국가별 GNI·인구 데이터 읽기
print(df.head())  # 앞 5행 확인

fig = px.treemap(data_frame=df,  # df 이름
                 path=['continent', 'iso3'],  # 데이터의 계층 구조
                 values='population',  # 타일 면적 기준 컬럼
                 color='GNI',  # 색 온도 기준 컬럼
                 color_continuous_scale='Bluyl'  # 컬러 팔레트
                 )

plt.axis('off')  # 축 눈금 제거
fig.update_layout(margin_t=50, margin_l=25,  # 여백 설정
                  margin_r=25, margin_b=25,
                  width=800,  # 그래프의 폭(pixel)
                  height=600,  # 그래프의 높이(pixel)
                  title_text='GNI 2014',  # 그래프 제목
                  title_font_size=20  # 제목 폰트 크기
                  )

# 그래프 저장 & 화면에 표시하기
html_path = Path('treemap.html').resolve()  # 현재 실행 폴더에 저장할 파일 경로
fig.write_html(html_path)  # html 파일로 결과 저장
webbrowser.open(html_path.as_uri())  # 웹 브라우저에서 그래프 확인
