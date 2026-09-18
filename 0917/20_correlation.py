# 여러 변수 간 상관계수
import pandas as pd
from pathlib import Path

# 이 파일의 위치를 기준으로 데이터 폴더를 찾는다(어느 폴더에서 실행해도 동작)
DATA_DIR = Path(__file__).resolve().parents[1] / 'data'

df = pd.read_csv(DATA_DIR / 'iris.csv')
df2 = df.loc[:, ~df.columns.isin(['Species'])]  # 품종 컬럼 제외

print(f'\n[df2.corr()] 4개 변수 간 상관성 분석\n{df2.corr()}')
