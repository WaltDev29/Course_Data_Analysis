import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
from pathlib import Path

# 이 파일의 위치를 기준으로 데이터 폴더를 찾는다(어느 폴더에서 실행해도 동작)
DATA_DIR = Path(__file__).resolve().parents[1] / 'data'

df = pd.read_csv(DATA_DIR / 'wilcoxon_test.csv')
print(df)

# 데이터 탐색
print(df.mean())  # 그룹별 평균
print((df['post']-df['pre']).mean())  # pre, post 차이의 평균

fig, axes = plt.subplots(nrows=1, ncols=2)
df['pre'].plot.box(grid=False, ax=axes[0])
plt.ylim([60, 100])
df['post'].plot.box(grid=False, ax=axes[1])
plt.show()

# 윌콕슨 부호순위 검정
result = stats.wilcoxon(df['pre'], df['post'])
print(result)

# 윌콕슨 부호순위 검정 결과 시각화
import numpy as np
import itertools
plt.rcParams['font.family'] = 'Malgun Gothic'  # 한글 폰트(윈도우)
plt.rcParams['axes.unicode_minus'] = False
colors = ['#2a78d6', '#eb6834']  # 증가: 파랑, 감소: 주황

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 4.5))

# (1) 사람별 pre → post 변화와 중앙값 변화
for _, r in df.iterrows():
    c = colors[0] if r['post'] >= r['pre'] else colors[1]  # 점수가 오르면 파랑, 내리면 주황
    ax1.plot([0, 1], [r['pre'], r['post']], color=c, alpha=0.5, marker='o', markersize=5)
ax1.plot([0, 1], [df['pre'].median(), df['post'].median()], color='#0b0b0b',
         linewidth=3, marker='o', markersize=9, label='중앙값')
ax1.text(-0.05, df['pre'].median(), f"{df['pre'].median():g}", ha='right', va='center', fontsize=10)
ax1.text(1.05, df['post'].median(), f"{df['post'].median():g}", ha='left', va='center', fontsize=10)
ax1.plot([], [], color=colors[0], label='점수 증가')  # 범례용
ax1.plot([], [], color=colors[1], label='점수 감소')
ax1.set_xticks([0, 1], ['pre', 'post'])
ax1.set_xlim(-0.4, 1.8)
ax1.set_ylabel('점수')
ax1.set_title(f'사람별 점수 변화 (p = {result.pvalue:.4f})')
ax1.legend(frameon=False, loc='center right')
ax1.grid(axis='y', alpha=0.3)

# (2) 부호순위: 차이의 절댓값에 순위를 매기고 원래 부호를 붙인다
d = df['post'] - df['pre']  # 차이
rank = d.abs().rank()  # 같은 값은 평균 순위
signed = rank * np.sign(d)
w_plus, w_minus = rank[d > 0].sum(), rank[d < 0].sum()
order = signed.sort_values().index  # 부호순위 순서대로 정렬
bar_colors = [colors[0] if signed[i] > 0 else colors[1] for i in order]
ax2.bar(range(len(order)), signed[order], color=bar_colors)
for k, i in enumerate(order):  # 막대 끝에 원래 차이 표시
    ax2.text(k, signed[i] + (0.2 if signed[i] > 0 else -0.2), f'{d[i]:+g}',
             ha='center', va='bottom' if signed[i] > 0 else 'top', fontsize=9)
ax2.axhline(0, color='#52514e', linewidth=1)
ax2.bar(0, 0, color=colors[0], label=f'증가 순위합 W+ = {w_plus:g}')  # 범례용
ax2.bar(0, 0, color=colors[1], label=f'감소 순위합 W- = {w_minus:g}')
ax2.set_xticks(range(len(order)), [f'{i + 1}번' for i in order])
ax2.set_ylim(-9.5, 9.5)
ax2.set_ylabel('부호순위')
ax2.set_title('부호순위 (막대 위 숫자는 post - pre)')
ax2.legend(frameon=False, loc='upper left')
ax2.grid(axis='y', alpha=0.3)

# (3) 귀무가설에서 W의 정확분포: 순위 1~n에 +, - 부호를 붙이는 모든 경우(2^n가지)
# 표본이 작고 차이가 0인 쌍이 없으면 scipy는 정규근사 대신 이 정확분포로 p-value를 계산한다
n = len(d)
all_w = [sum(k for k, s in zip(range(1, n + 1), signs) if s)
         for signs in itertools.product([0, 1], repeat=n)]  # 경우마다 + 순위의 합
w_values, counts = np.unique(all_w, return_counts=True)
prob = counts / counts.sum()
cum = np.cumsum(prob)
w_crit = w_values[cum <= 0.025].max()  # 한쪽 꼬리 확률이 0.025 이하인 가장 큰 W
max_w = n * (n + 1) // 2  # W의 최댓값
in_reject = (w_values <= w_crit) | (w_values >= max_w - w_crit)
ax3.bar(w_values, prob, color=np.where(in_reject, '#e34948', '#c3c2b7'), width=0.8)
ax3.bar(0, 0, color='#e34948', label=f'기각역 (W ≤ {w_crit} 또는 W ≥ {max_w - w_crit})')  # 범례용
ax3.axvline(result.statistic, color=colors[0], linewidth=2, label=f'W = {result.statistic:g}')
ax3.axvline(max_w - result.statistic, color=colors[0], linewidth=2, linestyle='--')  # 반대쪽 대칭 위치
print('정확분포 p =', 2 * prob[w_values <= result.statistic].sum())  # scipy의 p-value와 같다

# 정규근사 곡선 겹쳐 그리기: n이 크면 W는 정규분포에 가까워진다
mu = n * (n + 1) / 4  # W의 평균
sigma = np.sqrt(n * (n + 1) * (2 * n + 1) / 24)  # W의 표준편차
approx = stats.wilcoxon(df['pre'], df['post'], method='approx')  # 정규근사로 구한 p-value
x = np.linspace(0, max_w, 300)
ax3.plot(x, stats.norm.pdf(x, mu, sigma), color='#0b0b0b', linewidth=2,
         label=f'정규근사 N({mu:g}, {sigma:.2f}²), p = {approx.pvalue:.3f}')
ax3.bar(0, 0, color='#c3c2b7', label=f'정확분포, p = {result.pvalue:.3f}')  # 범례용
ax3.set_ylim(0, prob.max() * 1.45)  # 범례 자리 확보
ax3.set_xlabel('W (순위합)')
ax3.set_ylabel('확률')
ax3.set_title(f'W의 정확분포 (n = {n})에서 검정통계량의 위치')
ax3.legend(loc='upper left', fontsize=9, facecolor='white', edgecolor='none', framealpha=1)  # 세로선 위에 범례가 보이도록 흰 배경
ax3.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()