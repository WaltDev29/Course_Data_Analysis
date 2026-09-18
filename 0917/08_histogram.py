import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 이 파일의 위치를 기준으로 데이터 폴더를 찾는다(어느 폴더에서 실행해도 동작)
DATA_DIR = Path(__file__).resolve().parents[1] / 'data'

# 데이터 준비
df = pd.read_csv(DATA_DIR / 'cars.csv')
dist = df['dist']  # 제동거리
print(f'\n[dist] 제동거리\n{dist}')

# 구간 개수를 지정하여 히스토그램 그리기
dist.plot.hist()  # 기본 그래프
plt.show()

dist.plot.hist(bins=6)  # 막대 개수 지정
plt.show()

# 구간별 빈도수 계산
print(f'\n[dist.value_counts(bins=6, sort=False)] 구간별 빈도수\n'
      f'{dist.value_counts(bins=6, sort=False)}')

dist.plot.hist(bins=6,  # 막대 개수 지정
               title='Braking distance',  # 그래프 제목
               xlabel='distance',  # x축 레이블
               ylabel='frequency',  # y축 레이블
               color='g')  # 막대 색
plt.show()
