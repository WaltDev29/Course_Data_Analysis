import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
from pathlib import Path

# 이 파일의 위치를 기준으로 데이터 폴더를 찾는다(어느 폴더에서 실행해도 동작)
DATA_DIR = Path(__file__).resolve().parents[1] / 'data'

df = pd.read_csv(DATA_DIR / 'ind_ttest.csv')

# 데이터 탐색
print(df.head())
print(df.groupby('group').count())  # 그룹별 표본 크기
print(df.groupby('group').mean())  # 그룹별 평균
df.groupby('group').boxplot(grid=False)
plt.show()

group_1 = df.loc[df.group == 'A', 'height']
group_2 = df.loc[df.group == 'B', 'height']
print(group_1)
print(group_2)

# 정규성 검정
print(stats.shapiro(group_1))
print(stats.shapiro(group_2))

# 등분산성 검정
print(stats.levene(group_1, group_2))

# 독립표본 t-검정
result = stats.ttest_ind(group_1, group_2, equal_var=True)
print(result)

# t-검정 결과 시각화
import numpy as np
plt.rcParams['font.family'] = 'Malgun Gothic'  # 한글 폰트(윈도우)
plt.rcParams['axes.unicode_minus'] = False
colors = ['#2a78d6', '#eb6834']  # A: 파랑, B: 주황

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))

# (1) 그룹별 평균과 95% 신뢰구간 + 개별 관측값
for i, (name, g) in enumerate([('A', group_1), ('B', group_2)]):
    ci = stats.t.interval(0.95, len(g) - 1, loc=g.mean(), scale=stats.sem(g))  # 95% 신뢰구간
    x = np.random.normal(i, 0.06, len(g))  # 점이 겹치지 않게 좌우로 흩뿌림
    ax1.scatter(x, g, color=colors[i], alpha=0.35, s=20)
    ax1.errorbar(i + 0.25, g.mean(), yerr=[[g.mean() - ci[0]], [ci[1] - g.mean()]],
                 fmt='o', color=colors[i], markersize=8, capsize=6, linewidth=2)
    ax1.text(i + 0.33, g.mean(), f'평균 {g.mean():.2f}', va='center', fontsize=10)
ax1.set_xticks([0, 1], ['A 그룹', 'B 그룹'])
ax1.set_xlim(-0.5, 1.8)
ax1.set_ylabel('height')
ax1.set_title(f'그룹별 평균과 95% 신뢰구간 (p = {result.pvalue:.4f})')
ax1.grid(axis='y', alpha=0.3)

# (2) t-분포에서 검정통계량 위치와 기각역(유의수준 0.05, 양측)
dof = len(group_1) + len(group_2) - 2  # 자유도
t_crit = stats.t.ppf(0.975, dof)  # 임계값
x = np.linspace(-4.5, 4.5, 500)
y = stats.t.pdf(x, dof)
ax2.plot(x, y, color='#52514e', linewidth=2)
ax2.fill_between(x, y, where=(x <= -t_crit), color='#e34948', alpha=0.3, label='기각역 (α = 0.05)')
ax2.fill_between(x, y, where=(x >= t_crit), color='#e34948', alpha=0.3)
ax2.axvline(result.statistic, color=colors[0], linewidth=2, label=f't = {result.statistic:.2f}')
ax2.text(-t_crit - 0.15, stats.t.pdf(t_crit, dof) + 0.02, f'-{t_crit:.2f}', ha='right', fontsize=9)
ax2.text(t_crit + 0.15, stats.t.pdf(t_crit, dof) + 0.02, f'{t_crit:.2f}', ha='left', fontsize=9)
ax2.set_xlabel('t 값')
ax2.set_ylabel('확률밀도')
ax2.set_title(f't-분포 (자유도 {dof})에서 검정통계량의 위치')
ax2.legend(frameon=False)
ax2.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()
