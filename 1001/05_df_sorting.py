# 데이터프레임 정렬(오름차순, 내림차순, 여러 기준)
import pandas as pd
from pathlib import Path

# 이 파일의 위치를 기준으로 데이터 폴더를 찾는다(어느 폴더에서 실행해도 동작)
DATA_DIR = Path(__file__).resolve().parents[2] / 'data'

df = pd.read_csv(DATA_DIR / 'iris.csv')

# 데이터프레임의 정렬
# 오름차순 정렬(작은 값부터, 기본값)
df_sorted = df.sort_values('Sepal_Length')
print('[Sepal_Length 오름차순 정렬]', df_sorted.head(10), sep='\n')

# 내림차순 정렬(큰 값부터)
df_sorted = df.sort_values('Sepal_Length', ascending=False)
print('[Sepal_Length 내림차순 정렬]', df_sorted.head(10), sep='\n')

# 여러 개의 기준 컬럼 적용
# Species로 먼저 정렬하고, 품종이 같으면 Sepal_Width로 정렬
df_sorted = df.sort_values(['Species', 'Sepal_Width'])
print('[Species, Sepal_Width 기준 정렬]', df_sorted.head(10), sep='\n')
