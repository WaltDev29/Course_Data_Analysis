import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
from pathlib import Path

# 이 파일의 위치를 기준으로 데이터 폴더를 찾는다(어느 폴더에서 실행해도 동작)
DATA_DIR = Path(__file__).resolve().parents[1] / 'data'

df = pd.read_csv(DATA_DIR / 'mw_test.csv')

# 데이터 탐색
print(df.head())
print(df.groupby('group').count())  # 그룹별 표본 크기
print(df.groupby('group').mean())  # 그룹별 평균
df.groupby('group').boxplot(grid=False)
plt.show()

group_1 = df.loc[df.group == 'A', 'score']
group_2 = df.loc[df.group == 'B', 'score']

# 맨 휘트니 U 검정
result = stats.mannwhitneyu(group_1, group_2)
print(result)

# 맨 휘트니 U 검정 결과 시각화
plt.rcParams['font.family'] = 'Malgun Gothic'  # 한글 폰트(윈도우)
plt.rcParams['axes.unicode_minus'] = False
colors = {'A': '#2a78d6', 'B': '#eb6834'}  # A: 파랑, B: 주황

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 4.5))

# (1) 그룹별 점수와 중앙값(비모수 검정은 평균 대신 중앙값으로 본다)
for i, (name, g) in enumerate([('A', group_1), ('B', group_2)]):
    ax1.scatter([i] * len(g), g, color=colors[name], s=60, alpha=0.7)
    ax1.hlines(g.median(), i - 0.2, i + 0.2, color='#0b0b0b', linewidth=2)
    ax1.text(i + 0.25, g.median(), f'중앙값 {g.median():g}', va='center', fontsize=10)
ax1.set_xticks([0, 1], ['A 그룹', 'B 그룹'])
ax1.set_xlim(-0.5, 1.8)
ax1.set_ylabel('score')
ax1.set_title(f'그룹별 점수와 중앙값 (p = {result.pvalue:.4f})')
ax1.grid(axis='y', alpha=0.3)

# (2) 두 그룹을 합쳐 매긴 순위: 한 그룹이 한쪽 끝에 몰릴수록 차이가 크다
rank = df.assign(순위=df['score'].rank()).sort_values('순위')  # 같은 값은 평균 순위
for name in ['A', 'B']:
    part = rank[rank['group'] == name]
    y = 1 if name == 'A' else 0
    ax2.scatter(part['순위'], [y] * len(part), color=colors[name], s=200, alpha=0.8,
                label=f"{name} 그룹 (순위합 {part['순위'].sum():g})")
    for _, r in part.iterrows():
        ax2.text(r['순위'], y + 0.25, f"{r['score']:g}", ha='center', fontsize=9)  # 원래 점수
ax2.set_yticks([0, 1], ['B', 'A'])
ax2.set_ylim(-0.6, 1.8)
ax2.set_xticks(range(1, len(df) + 1))
ax2.set_xlabel('전체 순위 (점 위 숫자는 원래 점수)')
ax2.set_title(f'두 그룹을 합친 순위 (U = {result.statistic:g})')
ax2.legend(frameon=False, loc='upper left')
ax2.grid(axis='x', alpha=0.3)

# (3) 표준정규분포에서 z 값 위치와 기각역(유의수준 0.05, 양측)
# 동점이 있으면 scipy는 U를 정규분포로 근사해 p-value를 계산한다
import numpy as np
n1, n2 = len(group_1), len(group_2)
n = n1 + n2
ties = df['score'].value_counts()  # 값별 개수(2 이상이면 동점)
mu = n1 * n2 / 2  # U의 평균
sigma = np.sqrt(n1 * n2 / 12 * ((n + 1) - ((ties**3 - ties).sum()) / (n * (n - 1))))  # 동점 보정한 U의 표준편차
z = (result.statistic - mu + 0.5) / sigma  # 연속성 보정 0.5
print('z =', z, ', p =', 2 * stats.norm.cdf(z))  # scipy의 p-value와 같다

z_crit = stats.norm.ppf(0.975)  # 임계값 1.96
x = np.linspace(-4, 4, 500)
y = stats.norm.pdf(x)
ax3.plot(x, y, color='#52514e', linewidth=2)
ax3.fill_between(x, y, where=(x <= -z_crit), color='#e34948', alpha=0.3, label='기각역 (α = 0.05)')
ax3.fill_between(x, y, where=(x >= z_crit), color='#e34948', alpha=0.3)
ax3.axvline(z, color=colors['A'], linewidth=2, label=f'z = {z:.2f}')
ax3.text(-z_crit - 0.15, stats.norm.pdf(z_crit) + 0.02, f'-{z_crit:.2f}', ha='right', fontsize=9)
ax3.text(z_crit + 0.15, stats.norm.pdf(z_crit) + 0.02, f'{z_crit:.2f}', ha='left', fontsize=9)
ax3.set_xlabel('z 값')
ax3.set_ylabel('확률밀도')
ax3.set_title('표준정규분포에서 z 값의 위치')
ax3.legend(frameon=False)
ax3.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()
