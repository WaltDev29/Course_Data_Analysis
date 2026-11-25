# 피마 인디언 당뇨병 데이터로 KNN 분류 모델을 만들고 평가·예측하는 예제
import pandas as pd  # 데이터 처리 라이브러리
from sklearn.preprocessing import StandardScaler  # 표준화(평균 0, 표준편차 1)
from sklearn.model_selection import train_test_split  # 훈련용·검증용 데이터 분리
from sklearn.neighbors import KNeighborsClassifier as KNC  # K-최근접 이웃 분류 모델
from pathlib import Path  # 파일 경로 처리용

# 이 파일의 위치를 기준으로 데이터 폴더를 찾는다(어느 폴더에서 실행해도 동작)
DATA_DIR = Path(__file__).resolve().parents[1] / 'data'

# 데이터 준비
df = pd.read_csv(DATA_DIR / 'PimaIndiansDiabetes.csv')
print(df.head())
print(df.groupby('diabetes')['diabetes'].count())  # 당뇨병 음성(neg)·양성(pos) 인원 수

X = df.drop('diabetes', axis=1)  # 독립변수(입력): 임신 횟수, 혈당, 혈압 등 8개 열
y = df['diabetes']  # 종속변수(정답): 당뇨병 여부

# 데이터 표준화: KNN은 거리로 이웃을 찾으므로 열마다 범위를 맞춘다
scaler = StandardScaler()
scaler.fit(X)  # 열별 평균·표준편차 계산
result = scaler.transform(X)  # 계산한 값으로 변환
X_scaled = pd.DataFrame(result, columns=X.columns)
print(X_scaled.head())

# 훈련용, 검증용 데이터 분리
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y,
    test_size=0.3,  # 30%를 검증용으로 사용
    random_state=123,  # 실행할 때마다 같게 나뉘도록 고정
    stratify=y)  # 훈련용·검증용의 neg/pos 비율을 원래 데이터와 같게 유지

# 모델 생성
knn = KNC(n_neighbors=3)  # 가장 가까운 이웃 3개의 다수결로 분류
knn.fit(X_train, y_train)  # 훈련용 데이터로 학습

# 모델 평가: 정확도(accuracy)
print(knn.score(X_test, y_test))  # 검증용 데이터에서 맞힌 비율

# 모델 활용
# 1명의 환자 예측
data = pd.DataFrame([[8, 182, 64, 0, 0, 23, 0.67, 32]],  # 열 순서: pregnant, glucose, pressure, triceps, insulin, mass, pedigree, age
                    columns=X_test.columns)
data = scaler.transform(data)  # 새 데이터도 훈련 때와 같은 기준(scaler)으로 표준화
patient = pd.DataFrame(data,
                       columns=X_test.columns)
print(patient)

pred = knn.predict(patient)  # 예측 결과: 'neg' 또는 'pos'
print(pred)

# 여러 명의 환자 예측
pred = knn.predict(X_test)  # 검증용 데이터 전체 예측
print(pred)
