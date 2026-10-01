# 컬럼 값의 순위 구하기
import pandas as pd
from pathlib import Path

# 이 파일의 위치를 기준으로 데이터 폴더를 찾는다(어느 폴더에서 실행해도 동작)
DATA_DIR = Path(__file__).resolve().parents[2] / 'data'

df = pd.read_csv(DATA_DIR / 'iris.csv')

# 순위
# rank(): 값이 같으면 평균 순위(예: 2.5)를 주므로 astype(int)로 정수 변환(소수점 버림)
print('[Petal_Length 오름차순 순위]', df['Petal_Length'].rank().astype(int), sep='\n') # 오름차순 순위(작은 값이 1위)
print('[Petal_Length 내림차순 순위]', df['Petal_Length'].rank(ascending = False).astype(int), sep='\n') # 내림차순 순위(큰 값이 1위)