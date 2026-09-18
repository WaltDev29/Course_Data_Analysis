import pandas as pd
from scipy import stats

# 평균 계산 방식
ds = [60, 62, 64, 65, 68, 69]
weight = pd.Series(ds)
ds.append(120)  # ds에 120 추가
weight_heavy = pd.Series(ds)
print(f'\n[weight] 120 추가 전 데이터\n{weight}')
print(f'\n[weight_heavy] 120 추가 후 데이터\n{weight_heavy}')

print(f'\n[weight.mean()] 평균: {weight.mean()}')
print(f'\n[weight_heavy.mean()] 평균: {weight_heavy.mean()}')

print(f'\n[weight.median()] 중앙값: {weight.median()}')
print(f'\n[weight_heavy.median()] 중앙값: {weight_heavy.median()}')

print(f'\n[stats.trim_mean(weight, 0.2)] 절사평균(상하위 20% 제외): '
      f'{stats.trim_mean(weight, 0.2)}')
print(f'\n[stats.trim_mean(weight_heavy, 0.2)] 절사평균(상하위 20% 제외): '
      f'{stats.trim_mean(weight_heavy, 0.2)}')
