import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
from pathlib import Path

# 이 파일의 위치를 기준으로 데이터 폴더를 찾는다(어느 폴더에서 실행해도 동작)
DATA_DIR = Path(__file__).resolve().parents[1] / 'data'

df = pd.read_csv(DATA_DIR / 'paired_ttest.csv')

# 데이터 탐색
print(df.head())
print(df[['before', 'after']].mean())  # 그룹별 평균
print((df['after']-df['before']).mean())  # before, after 차이의 평균

fig, axes = plt.subplots(nrows=1, ncols=2)
df['before'].plot.box(grid=False, ax=axes[0])
plt.ylim([60, 100])
df['after'].plot.box(grid=False, ax=axes[1])
plt.show()

# 정규성 검정
print(stats.shapiro(df['after']-df['before']))

# 대응표본 t-검정
result = stats.ttest_rel(df['before'], df['after'])
print(result)

# 대응표본 t-검정 결과 시각화
import numpy as np
plt.rcParams['font.family'] = 'Malgun Gothic'  # 한글 폰트(윈도우)
plt.rcParams['axes.unicode_minus'] = False
colors = ['#2a78d6', '#eb6834']  # 증가: 파랑, 감소: 주황

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))

# (1) 학생별 before → after 변화와 평균 변화
for _, r in df.iterrows():
    c = colors[0] if r['after'] >= r['before'] else colors[1]  # 점수가 오르면 파랑, 내리면 주황
    ax1.plot([0, 1], [r['before'], r['after']], color=c, alpha=0.4, marker='o', markersize=5)
ax1.plot([0, 1], [df['before'].mean(), df['after'].mean()], color='#0b0b0b',
         linewidth=3, marker='o', markersize=9, label='평균')
ax1.text(-0.05, df['before'].mean(), f"{df['before'].mean():.1f}", ha='right', va='center', fontsize=10)
ax1.text(1.05, df['after'].mean(), f"{df['after'].mean():.1f}", ha='left', va='center', fontsize=10)
ax1.plot([], [], color=colors[0], label='점수 증가')  # 범례용
ax1.plot([], [], color=colors[1], label='점수 감소')
ax1.set_xticks([0, 1], ['before', 'after'])
ax1.set_xlim(-0.4, 1.8)
ax1.set_ylabel('점수')
ax1.set_title(f'학생별 점수 변화 (p = {result.pvalue:.4f})')
ax1.legend(frameon=False, loc='center right')
ax1.grid(axis='y', alpha=0.3)

# (2) t-분포에서 검정통계량 위치와 기각역(유의수준 0.05, 양측)
dof = len(df) - 1  # 자유도(쌍의 개수 - 1)
t_crit = stats.t.ppf(0.975, dof)  # 임계값
lim = max(4.5, abs(result.statistic) + 1)
x = np.linspace(-lim, lim, 500)
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
