import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 이 파일의 위치를 기준으로 데이터 폴더를 찾는다(어느 폴더에서 실행해도 동작)
DATA_DIR = Path(__file__).resolve().parents[1] / 'data'

# 데이터 읽기
df = pd.read_csv(DATA_DIR / 'iris.csv')

# 화면 분할 정의
fig, axes = plt.subplots(nrows=2, ncols=2)

# 각 분할 영역에 그래프 작성하기
df['Petal_Length'].plot.hist(ax=axes[0, 0])
df['Petal_Length'].plot.box(ax=axes[0, 1])

fd = df['Species'].value_counts()
fd.plot.pie(ax=axes[1, 0])
fd.plot.barh(ax=axes[1, 1])

# 통합 그래프에 제목 지정
fig.suptitle('Multiple Graph Example', fontsize=14)

plt.tight_layout()

# 분할 그래프 화면에 나타내기
plt.show()
