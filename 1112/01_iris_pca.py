# iris 데이터를 표준화한 뒤 PCA로 2차원 축소해 산점도로 그리는 예제
import pandas as pd  # 데이터 처리 라이브러리
from sklearn.preprocessing import StandardScaler  # 표준화(평균 0, 표준편차 1)
from sklearn.decomposition import PCA  # 주성분 분석(차원 축소)
import matplotlib.pyplot as plt  # 그래프 출력용 라이브러리
from pathlib import Path  # 파일 경로 처리용

# 이 파일의 위치를 기준으로 데이터 폴더를 찾는다(어느 폴더에서 실행해도 동작)
DATA_DIR = Path(__file__).resolve().parents[1] / 'data'

# 데이터 준비
df = pd.read_csv(DATA_DIR / 'iris.csv')
df = df.drop('Species', axis=1)  # 품종(정답) 열은 빼고 측정값 4개만 사용
print(df.head())

# 데이터 표준화: 열마다 단위·범위가 달라도 같은 기준으로 비교할 수 있게 한다
scaler = StandardScaler()
result = scaler.fit_transform(df)  # 평균·표준편차 계산(fit)과 변환(transform)을 한 번에
df_scaled = pd.DataFrame(result, columns=df.columns)  # 결과가 배열이므로 데이터프레임으로 되돌림
print(df_scaled.head())

# 차원 축소: 4개 열의 정보를 최대한 보존하면서 2개 축(주성분)으로 줄인다
pca = PCA(n_components=2)  # 남길 주성분 개수
transform = pca.fit_transform(df_scaled)  # 2차원으로 축소
transform = pd.DataFrame(transform)  # 열 이름은 0(첫째 주성분), 1(둘째 주성분)
print(transform.head())

# 시각화
transform.plot.scatter(x=0, y=1,  # 산점도
                       title='PCA plot')
plt.show()
