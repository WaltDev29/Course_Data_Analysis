# 품종별 그룹 집계(평균, 표준편차)
import pandas as pd
from pathlib import Path

# 이 파일의 위치를 기준으로 데이터 폴더를 찾는다(어느 폴더에서 실행해도 동작)
DATA_DIR = Path(__file__).resolve().parents[2] / 'data'

df = pd.read_csv(DATA_DIR / 'iris.csv')

# groupby: Species 값이 같은 행끼리 묶은 뒤 컬럼별로 집계
df_agg = df.groupby('Species').mean()  # 평균
print('[품종별 평균]', df_agg, sep='\n')

df_agg = df.groupby('Species').std()  # 표준편차
print('[품종별 표준편차]', df_agg, sep='\n')
