import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 이 파일의 위치를 기준으로 데이터 폴더를 찾는다(어느 폴더에서 실행해도 동작)
DATA_DIR = Path(__file__).resolve().parents[1] / 'data'
state = pd.read_csv(DATA_DIR / 'state_x77.csv')
division = pd.read_csv(DATA_DIR / 'state_division.csv')
state['division'] = division
print(f'\n[state.head()] 데이터 앞부분 일부\n{state.head()}')

state.plot.scatter(x='Illiteracy', y='Income')
plt.show()
print(f"\n[state['Illiteracy'].corr(state['Income'])] 상관계수: "
      f"{state['Illiteracy'].corr(state['Income'])}")

state.plot.scatter(x='Income', y='Life_Exp')
plt.show()
print(f"\n[state['Income'].corr(state['Life_Exp'])] 상관계수: "
      f"{state['Income'].corr(state['Life_Exp'])}")

pd.plotting.scatter_matrix(state, figsize=(10, 10))
plt.show()

state_tmp = state.drop(['State', 'division'], axis=1)
print(f'\n[state_tmp.corr()] 변수 간 상관계수\n{state_tmp.corr()}')

pop = state.groupby('division')['Population'].sum()
print(f'\n[pop] 지역별 주의 인구수 합계\n{pop}')
pop.plot.bar()
plt.xlabel('Division')
plt.ylabel('Population')
plt.title('Population by Division')
plt.subplots_adjust(bottom=0.3)
plt.show()

dict = {'East South Central': 'black', 'Pacific': 'grey', 'Mountain': 'brown',
        'West South Central': 'red', 'New England': 'orange',
        'South Atlantic': 'green', 'East North Central': 'blue',
        'West North Central': 'cyan', 'Middle Atlantic': 'purple'}
colors = list(dict[key] for key in state.division)  # 각 점의 색을 지정

state.plot.scatter(x='HS_Grad', y='Income', c=colors)
plt.show()
