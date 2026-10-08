# 미국 주별 범죄율 데이터로 버블 차트를 그리는 예제
import pandas as pd  # 데이터 처리 라이브러리
import seaborn as sns  # 통계 시각화 라이브러리
import matplotlib.pyplot as plt  # 그래프 출력용 라이브러리
from pathlib import Path  # 파일 경로 처리용

# 이 파일의 위치를 기준으로 데이터 폴더를 찾는다(어느 폴더에서 실행해도 동작)
DATA_DIR = Path(__file__).resolve().parents[2] / 'data'

df = pd.read_csv(DATA_DIR / 'crimeRatesByState2005.csv')  # 2005년 미국 주별 범죄율 데이터 읽기
print(df.head())  # 앞 5행 확인

# 버블 차트
sns.set_theme(rc={'figure.figsize': (7, 7)})  # 그림 크기 7x7인치

sns.scatterplot(
    data=df,  # df 이름
    x="murder",  # x축
    y="burglary",  # y축
    size="population",  # 원의 크기
    sizes=(20, 4000),  # 원의 크기 범위
    hue="state",  # 원의 색
    alpha=0.5,  # 투명도
    legend=False  # 범례 표시 여부
)
plt.xlim(0, 12)  # x축 값의 범위

# 주 이름을 버블 위에 표시
for i in range(0, df.shape[0]):  # 데이터 행 수만큼 반복
    plt.text(x=df.murder[i], y=df.burglary[i], s=df.state[i],  # 버블 중심 좌표에 주 이름 출력
         horizontalalignment='center', size='small', color='dimgray')  # 가운데 정렬, 작은 회색 글씨
plt.show()  # 그래프 화면에 출력
