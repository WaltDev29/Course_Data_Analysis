# KNN 방식으로 결측값을 추정해 채우기
import pandas as pd
from sklearn.impute import KNNImputer  # 가까운 이웃의 값으로 결측값을 추정하는 도구
from sklearn.preprocessing import MinMaxScaler  # 값을 0~1 범위로 변환하는 스케일러
from pathlib import Path

# 이 파일의 위치를 기준으로 데이터 폴더를 찾는다(어느 폴더에서 실행해도 동작)
DATA_DIR = Path(__file__).resolve().parents[1] / 'data'

df_org = pd.read_csv(DATA_DIR / 'iris.csv')  # 원본(나중에 추정값과 비교하는 용도)
df_miss = df_org.copy()  # 결측값을 만들 복사본(원본은 그대로 유지)

# 결측값 생성
df_miss.iloc[0, 3] = pd.NA ; df_miss.iloc[0, 2] = pd.NA
df_miss.iloc[1, 2] = None ; df_miss.iloc[2, 3] = None
print('[결측값 생성 후 앞부분]', df_miss.head(4), sep='\n')

# (1) 데이터 표준화
# KNN은 거리로 이웃을 찾으므로 컬럼마다 값의 범위를 맞춰야 함
scaler = MinMaxScaler()                         # 스케일러 정의
df_scaled = scaler.fit_transform(df_miss.iloc[:, :4]) # 표준화(숫자 컬럼 4개만, 결과는 넘파이 배열)
print('[표준화 결과]', df_scaled[0:5, :], sep='\n')

# (2) 결측값 추정
# n_neighbors=5: 가장 가까운 행 5개의 평균으로 결측값을 채움
imputer = KNNImputer(n_neighbors=5)             # 추정모델 정의
df_scaled = imputer.fit_transform(df_scaled)    # 결측값 추정
print('[결측값 추정 결과(표준화 값)]', df_scaled[0:5, :], sep='\n')

# (3) 표준화 이전으로 변환
df_filled = scaler.inverse_transform(df_scaled)  # 0~1 값을 원래 단위(cm)로 되돌림
print('[원래 척도로 변환한 결과]', df_filled[0:5, :], sep='\n')

df_miss.iloc[:,:4] = df_filled                  # 추정값 -> 결측값

# 추정값의 정확도 확인(두 결과를 비교해 추정값이 원래 값과 얼마나 가까운지 확인)
print('[결측값을 채운 데이터]', df_miss.head(4), sep='\n')
print('[원본 데이터]', df_org.head(4), sep='\n')