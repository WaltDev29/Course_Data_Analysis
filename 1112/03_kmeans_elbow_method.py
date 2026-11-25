# 12-2의 K-평균 군집화에 이어 엘보 방법으로 적절한 군집 개수(k)를 찾는 예제
import pandas as pd  # 데이터 처리 라이브러리
from sklearn.decomposition import PCA  # 주성분 분석(차원 축소)
from sklearn.cluster import KMeans  # K-평균 군집화
from sklearn.preprocessing import StandardScaler  # 표준화(평균 0, 표준편차 1)
import matplotlib.pyplot as plt  # 그래프 출력용 라이브러리
import seaborn as sns  # 통계 시각화 라이브러리
from pathlib import Path  # 파일 경로 처리용

# 이 파일의 위치를 기준으로 데이터 폴더를 찾는다(어느 폴더에서 실행해도 동작)
DATA_DIR = Path(__file__).resolve().parents[1] / 'data'

# 데이터 준비
df = pd.read_csv(DATA_DIR / 'iris.csv')
df = df.drop('Species', axis=1)  # 군집화는 정답 없이 하므로 품종 열을 뺀다
print(df.head())

# 데이터 표준화: 거리 기반 알고리즘이라 열마다 범위가 다르면 큰 값의 열이 결과를 좌우한다
scaler = StandardScaler()
result = scaler.fit_transform(df)
df_scaled = pd.DataFrame(result, columns=df.columns)
print(df_scaled.head())

# 군집화
model = KMeans(n_clusters=3,  # 만들 군집의 개수
               n_init=10,  # 시작 중심점을 바꿔 10번 실행하고 가장 좋은 결과를 사용
               random_state=123)  # 실행할 때마다 같은 결과가 나오도록 고정
model.fit(df_scaled)

# 군집화 결과 확인
print(model.cluster_centers_)  # 군집 중심점 좌표
print(model.labels_)  # 각 행의 군집 번호
print(model.inertia_)  # 군집 평가 점수(각 점과 중심점 거리 제곱의 합, 작을수록 잘 뭉침)

# 차원 축소: 4차원 데이터를 화면에 그리기 위해 2차원으로 줄인다
pca = PCA(n_components=2)
transform = pca.fit_transform(df_scaled)  # 2차원으로 축소
transform = pd.DataFrame(transform)
transform['cluster'] = model.labels_  # 군집 정보 추가
print(transform.head())

# 시각화
sns.scatterplot(
    data=transform,
    x=0,  # x축
    y=1,  # y축
    hue="cluster",  # 원의 색
    palette='Set2',  # 팔레트 선택
    legend=False  # 범례 표시 여부
)

plt.show()

# 12-2에 이어서 실행

# 적절한 k-값 결정(엘보 방법): k를 1~9로 바꿔 가며 inertia를 구한다
ks = range(1, 10)  # 군집의 개수
inertias = pd.Series([])  # 군집화 평가 결과

for k in ks:
    model = KMeans(n_clusters=k,
                   n_init=10, random_state=123)
    model.fit(df_scaled)
    inertias.loc[k] = model.inertia_  # k를 인덱스로 inertia 저장

# k가 커질수록 inertia는 계속 줄어든다
# 감소 폭이 갑자기 완만해지는 지점(팔꿈치 모양)을 적절한 k로 고른다
plt.figure(figsize=(7, 4))
inertias.plot.line(title='Inertias Score',
                   xlabel='number of clusters, k',
                   ylabel='inertia')
plt.show()
