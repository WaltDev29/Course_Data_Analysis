import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Malgun Gothic' # 한글 폰트 설정
plt.rcParams['axes.unicode_minus'] = False # 마이너스 부호 깨짐 방지

hobby = pd.Series(['등산', '낚시', '골프', '수영', '등산', '등산',
                   '낚시', '수영', '등산', '낚시', '수영', '골프'])
print(f'\n[hobby] 취미 데이터\n{hobby}')

fd = hobby.value_counts()
print(f'\n[fd] 취미별 도수분포\n{fd}')

fig, axes = plt.subplots(nrows=1, ncols=2)  # 화면 분할 정의
fd.plot.bar(ax=axes[0])  # 막대그래프
fd.plot.pie(ax=axes[1])  # 원그래프
fig.suptitle('선호 취미 분포', fontsize=14)
plt.show()
