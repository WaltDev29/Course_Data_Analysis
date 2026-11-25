from scipy import stats

#남성의 정당A, B에 대한 지지 빈도, 여성의 정당A, B에 대한 지지 빈도
men = [10, 10]
women = [15, 65]

# 카이제곱 검정
result = stats.chi2_contingency([men, women])
print(result)

# 카이제곱 검정 결과 시각화
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Malgun Gothic'  # 한글 폰트(윈도우)
plt.rcParams['axes.unicode_minus'] = False
colors = ['#2a78d6', '#eb6834']  # 정당A: 파랑, 정당B: 주황

observed = np.array([men, women])
expected = result.expected_freq
rows, cols = ['남성', '여성'], ['정당A', '정당B']

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 4.5))

# (1) 성별 정당 지지 비율(100% 누적 막대)
ratio = observed / observed.sum(axis=1, keepdims=True) * 100
left = np.zeros(len(rows))
for j, name in enumerate(cols):
    ax1.barh(rows, ratio[:, j], left=left, color=colors[j], label=name, height=0.5)
    for i in range(len(rows)):
        ax1.text(left[i] + ratio[i, j] / 2, i, f'{ratio[i, j]:.1f}%\n({observed[i, j]}명)',
                 ha='center', va='center', color='white', fontsize=10)
    left += ratio[:, j]
ax1.set_xlim(0, 100)
ax1.set_xlabel('지지 비율 (%)')
ax1.set_title(f'성별 정당 지지 비율 (p = {result.pvalue:.4f})')
ax1.legend(frameon=False, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2)
ax1.invert_yaxis()  # 남성을 위에 표시

# (2) 관측빈도와 기대빈도 비교: 차이가 클수록 카이제곱 값이 커진다
# 2x2 표는 Yates 연속성 보정: (|관측 - 기대| - 0.5)² / 기대
labels = [f'{r}\n{c}' for r in rows for c in cols]
obs, exp = observed.ravel(), expected.ravel()
contrib = (np.abs(obs - exp) - 0.5) ** 2 / exp  # 칸별 카이제곱 기여도
x = np.arange(len(labels))
ax2.bar(x - 0.2, obs, width=0.4, color=[colors[j] for _ in rows for j in range(len(cols))])
ax2.bar(x + 0.2, exp, width=0.4, color='#c3c2b7', label='기대빈도')
ax2.bar(0, 0, color=colors[0], label='관측빈도 (정당A)')  # 범례용
ax2.bar(0, 0, color=colors[1], label='관측빈도 (정당B)')
for k in range(len(labels)):
    ax2.text(x[k], max(obs[k], exp[k]) + 1.5, f'기여도 {contrib[k]:.2f}', ha='center', fontsize=9)
ax2.set_xticks(x, labels)
ax2.set_ylim(0, max(obs.max(), exp.max()) * 1.2)
ax2.set_ylabel('빈도 (명)')
ax2.set_title(f'관측빈도와 기대빈도 (기여도 합 = χ² = {contrib.sum():.2f})')
ax2.legend(frameon=False, loc='upper left')
ax2.grid(axis='y', alpha=0.3)

# (3) 카이제곱분포에서 검정통계량 위치와 기각역(유의수준 0.05)
# 카이제곱 검정은 차이가 클수록 값이 커지므로 오른쪽 꼬리만 기각역이다
chi_crit = stats.chi2.ppf(0.95, result.dof)  # 임계값
x = np.linspace(0.01, max(10, result.statistic + 3), 500)
y = stats.chi2.pdf(x, result.dof)
ax3.plot(x, y, color='#52514e', linewidth=2)
ax3.fill_between(x, y, where=(x >= chi_crit), color='#e34948', alpha=0.3, label=f'기각역 (χ² ≥ {chi_crit:.2f})')
ax3.axvline(result.statistic, color=colors[0], linewidth=2, label=f'χ² = {result.statistic:.2f}')
ax3.set_ylim(0, 0.3)  # 자유도 1이면 0 근처에서 값이 매우 커지므로 위쪽을 잘라 꼬리를 크게 본다
ax3.set_xlabel('χ² 값')
ax3.set_ylabel('확률밀도')
ax3.set_title(f'카이제곱분포 (자유도 {result.dof})에서 검정통계량의 위치')
ax3.legend(frameon=False)
ax3.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()
