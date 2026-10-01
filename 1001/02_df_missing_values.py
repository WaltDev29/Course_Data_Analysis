# 데이터프레임의 결측값 확인과 제거
import pandas as pd
import numpy as np
from pathlib import Path

# 이 파일의 위치를 기준으로 데이터 폴더를 찾는다(어느 폴더에서 실행해도 동작)
DATA_DIR = Path(__file__).resolve().parents[2] / 'data'

# 결측값을 포함하는 데이터프레임 생성
df = pd.read_csv(DATA_DIR / 'iris.csv')
# pd.NA, np.nan, None 모두 판다스에서는 결측값으로 처리됨
df.iloc[0, 1] = pd.NA ; df.iloc[0, 2] = pd.NA  # 0행의 1, 2번 컬럼
df.iloc[1, 2] = np.nan ; df.iloc[2, 3] = None  # 1행의 2번 컬럼, 2행의 3번 컬럼
print('[결측값 생성 후 앞부분]', df.head(), sep='\n')

# 결측값 확인
print('[컬럼별 결측값 개수]', df.isnull().sum(), sep='\n') # 컬럼별 결측값 확인
print('[행별 결측값 개수]', df.isnull().sum(axis=1), sep='\n') # 행별 결측값 확인(axis=1: 가로 방향으로 합계)
print('[결측값이 있는 행]', df.loc[df.isnull().sum(axis=1)>0,:], sep='\n') # 결측값 행 출력(결측값이 1개 이상인 행만 선택)

# 결측값 제거
df = df.dropna() # 결측값이 있는 행 제거
df = df.reset_index(drop=True) # 인덱스 초기화
print('[결측값 제거 후 앞부분]', df.head(), sep='\n')