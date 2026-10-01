# 여러 컬럼 기준 그룹 집계(최댓값)
import pandas as pd
from pathlib import Path

# 이 파일의 위치를 기준으로 데이터 폴더를 찾는다(어느 폴더에서 실행해도 동작)
DATA_DIR = Path(__file__).resolve().parents[2] / 'data'

df = pd.read_csv(DATA_DIR / 'mtcars.csv')  # 자동차 32종의 성능 데이터

# cyl(실린더 수)과 vs(엔진 형태) 조합별로 묶어 각 컬럼의 최댓값 계산
df_agg = df.groupby(['cyl','vs']).max()
print('[cyl, vs별 최댓값]', df_agg, sep='\n')