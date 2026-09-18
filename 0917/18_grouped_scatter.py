import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 이 파일의 위치를 기준으로 데이터 폴더를 찾는다(어느 폴더에서 실행해도 동작)
DATA_DIR = Path(__file__).resolve().parents[1] / 'data'

# 데이터 읽기
df = pd.read_csv(DATA_DIR / 'iris.csv')

# 그룹이 있는 다중 산점도 작성
dict = {'setosa': 'red', 'versicolor': 'green', 'virginica': 'blue'}
colors = list(dict[key] for key in df.Species)  # 각 점의 색 지정
print(f'\n[colors] 각 점의 색\n{colors}')

df.plot.scatter(x='Petal_Length',  # x축 변수명
                y='Petal_Width',  # y축 변수명
                s=30,  # 점의 크기
                c=colors,  # 점의 색깔
                marker='o')  # 점의 모양
plt.show()


fig, ax = plt.subplots()

for label, data in df.groupby('Species'):
    ax.scatter(x=data['Petal_Length'], y=data['Petal_Width'],  s=30,
               c=dict[label], marker='o', label=label)
    print(data)

ax.set_xlabel('Petal_Length')
ax.set_ylabel('Petal_Width')    

plt.legend()
plt.show()