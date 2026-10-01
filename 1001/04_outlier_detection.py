# Z-score와 IQR로 특잇값(이상치) 찾기와 제거
import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path

# 이 파일의 위치를 기준으로 데이터 폴더를 찾는다(어느 폴더에서 실행해도 동작)
DATA_DIR = Path(__file__).resolve().parents[1] / 'data'

df = pd.read_csv(DATA_DIR / 'iris.csv')
sw = df.Sepal_Width  # 꽃받침 너비 컬럼만 사용

# Z-score 이용
# Z-score: 평균에서 표준편차의 몇 배만큼 떨어져 있는지(abs로 부호 제거)
z = np.abs(stats.zscore(sw))
outliers = sw[z > 2]  # 평균에서 표준편차 2배보다 멀리 떨어진 값을 특잇값으로 판단
print('[Z-score 기준 특잇값]', outliers, sep='\n')

# IQR 이용
Q1 = sw.quantile(0.25)  # 1사분위수(하위 25% 지점)
Q3 = sw.quantile(0.75)  # 3사분위수(하위 75% 지점)
IQR = Q3 - Q1  # 사분위 범위(가운데 50% 데이터의 폭)

# Q1 - 1.5×IQR보다 작거나 Q3 + 1.5×IQR보다 큰 값을 특잇값으로 판단
outliers = sw[(sw < Q1 - IQR*1.5) | (sw > Q3 + IQR*1.5)]
print('[IQR 기준 특잇값]', outliers, sep='\n')

# 특잇값 제거
clean = sw.loc[~sw.isin(outliers)]  # isin: 특잇값에 포함되는지 확인, ~: True/False 반전
print('[특잇값 제거 후 데이터 개수]', len(clean), sep='\n')
