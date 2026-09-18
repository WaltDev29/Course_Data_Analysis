import pandas as pd
import numpy as np

# 사분위수 계산
mydata = [60, 62, 64, 65, 68, 69, 120]
mydata = pd.Series(mydata)
print(f'\n[mydata.quantile(0.25)] Q1: {mydata.quantile(0.25)}')
print(f'\n[mydata.quantile(0.5)] Q2: {mydata.quantile(0.5)}')
print(f'\n[mydata.quantile(0.75)] Q3: {mydata.quantile(0.75)}')
print(f'\n[mydata.quantile([0.25, 0.5, 0.75])]\n'
      f'{mydata.quantile([0.25, 0.5, 0.75])}')

print(f'\n[mydata.quantile(np.arange(0, 1, 0.1))] 10% 단위로 구간을 나누어 계산\n'
      f'{mydata.quantile(np.arange(0, 1, 0.1))}')
print(f'\n[mydata.describe()] 사분위수를 포함한 요약 정보\n{mydata.describe()}')
