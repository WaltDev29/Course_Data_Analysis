import pandas as pd
import matplotlib.pyplot as plt

# 숫자로 표현된 범주형 데이터의 시각화
colors = pd.Series([2, 3, 2, 1, 1, 2, 2, 1, 3, 2, 1, 3, 2, 1, 2])

fd = colors.value_counts()  # 도수분포를 fd에 저장
print(f'\n[fd] 도수분포\n{fd}')
print(f'\n[fd.index] fd의 인덱스 출력\n{fd.index}')
fd.index = ['red', 'green', 'blue']  # 숫자 인덱스를 문자 인덱스로 변경
print(f'\n[fd] 인덱스 변경 후\n{fd}')

# 막대그래프 출력
fd.plot.bar(xlabel='Color', ylabel='Frequency', rot=0, title='Favorite Color')
plt.show()

# 원그래프 출력
fd.plot.pie(ylabel='', autopct='%1.0f%%', title='Favorite Color')
plt.show()
