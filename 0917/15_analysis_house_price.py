import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 이 파일의 위치를 기준으로 데이터 폴더를 찾는다(어느 폴더에서 실행해도 동작)
DATA_DIR = Path(__file__).resolve().parents[1] / 'data'
df = pd.read_csv(DATA_DIR / 'BostonHousing.csv')
house_price = df['medv']
print(f'\n[house_price] 주택 가격\n{house_price}')

print(f'\n[house_price.mean()] 평균: {house_price.mean()}')
print(f'\n[house_price.median()] 중앙값: {house_price.median()}')
print(f'\n[house_price.quantile([0.25, 0.5, 0.75])] 사분위수\n'
      f'{house_price.quantile([0.25, 0.5, 0.75])}')

quan = house_price.quantile([0.25, 0.5, 0.75])
bins = [house_price.min(), quan[0.25], quan[0.5], quan[0.75], house_price.
        max()]
labels = ['Q1', 'Q2', 'Q3', 'Q4']
grp = pd.cut(house_price, bins=bins, labels=labels)
avg = house_price.groupby(grp).mean()
avg.plot.bar()
plt.xlabel('Quartiles')
plt.ylabel('House Price')
plt.title('Average House Price by Quartiles')
plt.show()

house_price.plot.box()
plt.show()

house_price.plot.hist(bins=8)
plt.show()
