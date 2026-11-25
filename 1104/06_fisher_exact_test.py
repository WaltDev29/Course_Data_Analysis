from scipy import stats

Group_A = [7, 3]
Group_B = [2, 9]

# 기대 빈도
print(stats.chi2_contingency([Group_A, Group_B])[3])

# 피셔의 정확 검정
result = stats.fisher_exact([Group_A, Group_B])
print(result)

# 피셔의 정확 검정 결과 시각화
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Malgun Gothic'  # 한글 폰트(윈도우)
plt.rcParams['axes.unicode_minus'] = False
colors = ['#2a78d6', '#eb6834']  # 정답: 파랑, 오답: 주황

observed = np.array([Group_A, Group_B])
expected = stats.chi2_contingency(observed)[3]
rows, cols = ['A반', 'B반'], ['정답', '오답']  # 표 11-4 반별 정답과 오답 빈도

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 4.5))

# (1) 그룹별 비율(100% 누적 막대)
ratio = observed / observed.sum(axis=1, keepdims=True) * 100
left = np.zeros(len(rows))
for j, name in enumerate(cols):
    ax1.barh(rows, ratio[:, j], left=left, color=colors[j], label=name, height=0.5)
    for i in range(len(rows)):
        ax1.text(left[i] + ratio[i, j] / 2, i, f'{ratio[i, j]:.1f}%\n({observed[i, j]}명)',
                 ha='center', va='center', color='white', fontsize=10)
    left += ratio[:, j]
ax1.set_xlim(0, 100)
ax1.set_xlabel('비율 (%)')
ax1.set_title(f'반별 정답과 오답 비율 (오즈비 = {result.statistic:g}, p = {result.pvalue:.4f})')
ax1.legend(frameon=False, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2)
ax1.invert_yaxis()  # A반을 위에 표시

# (2) 기대빈도: 5 미만인 칸이 있으면 카이제곱 근사가 부정확해서 피셔 검정을 쓴다
labels = [f'{r}\n{c}' for r in rows for c in cols]
exp = expected.ravel()
x = np.arange(len(labels))
ax2.bar(x, exp, color=np.where(exp < 5, '#e34948', '#c3c2b7'), width=0.6)
for k in range(len(labels)):
    ax2.text(x[k], exp[k] - 0.15, f'{exp[k]:.2f}', ha='center', va='top', color='#0b0b0b', fontsize=10)
ax2.axhline(5, color='#0b0b0b', linewidth=1.5, linestyle='--', label='기준선 5')
ax2.bar(0, 0, color='#e34948', label='기대빈도 5 미만')  # 범례용
ax2.set_xticks(x, labels)
ax2.set_ylim(0, 8)
ax2.set_ylabel('기대빈도 (명)')
ax2.set_title(f'기대빈도 (5 미만: {(exp < 5).sum()}칸 / {len(exp)}칸)')
ax2.legend(frameon=False, loc='upper left')
ax2.grid(axis='y', alpha=0.3)


# (3) A반 정답자 수: 반과 정답이 무관할 때 기대되는 인원과 실제 인원 비교
# 차이가 클수록 우연히 생기기 어렵다 → 그 확률이 피셔 검정의 p-value
obs_a, exp_a = observed[0, 0], expected[0, 0]
ax3.barh([0, 1], [exp_a, obs_a], color=['#c3c2b7', colors[0]], height=0.5)
ax3.text(exp_a + 0.1, 0, f'{exp_a:.1f}명', va='center', fontsize=12)
ax3.text(obs_a + 0.1, 1, f'{obs_a}명', va='center', fontsize=12)
ax3.annotate('', xy=(obs_a, 0.5), xytext=(exp_a, 0.5),
             arrowprops=dict(arrowstyle='->', color='#0b0b0b', linewidth=1.5))  # 기대 → 실제 차이
ax3.text((exp_a + obs_a) / 2, 0.58, f'+{obs_a - exp_a:.1f}명', ha='center', fontsize=11)
ax3.set_yticks([0, 1], ['기대\n(무관할 때)', '실제\n(관측)'])
ax3.set_xlim(0, observed[:, 0].sum() + 0.5)  # 최대는 정답자 전체 인원
ax3.set_xlabel(f'{rows[0]} {cols[0]}자 수 (명)')
ax3.set_title(f'이 정도 차이가 우연히 생길 확률 p = {result.pvalue:.4f}')
ax3.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.show()
