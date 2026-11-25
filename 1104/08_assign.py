# -*- coding: utf-8 -*-
"""
과제: 하루치 주식시장 데이터(krx_20261007.csv) 가설 검정 및 시각화
- 검정 ① KOSPI와 KOSDAQ의 등락률 비교 (독립된 두 집단)
- 검정 ② 종가와 시가 비교 (대응 표본)
- 검정 ③ 시장과 상승·하락의 연관성 (범주형 두 변수)
"""

from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
from matplotlib import font_manager

# ---------------------------------------------------------
# 0. 환경 설정 및 데이터 로드
# ---------------------------------------------------------
installed_fonts = {f.name for f in font_manager.fontManager.ttflist}
font_name = next((f for f in ['Malgun Gothic', 'AppleGothic', 'NanumGothic', 'Noto Sans CJK KR'] if f in installed_fonts), None)
if font_name:
    plt.rcParams['font.family'] = font_name
plt.rcParams['axes.unicode_minus'] = False

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR.parent / 'data' / 'krx_20261007.csv'

try:
    df = pd.read_csv(DATA_PATH, encoding='cp949')
except UnicodeDecodeError:
    df = pd.read_csv(DATA_PATH, encoding='euc-kr')

num_cols = ['종가', '대비', '등락률', '시가', '고가', '저가', '거래량', '거래대금', '시가총액', '상장주식수']
for col in num_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')


# =========================================================
# 검정 ① KOSPI와 KOSDAQ의 등락률 비교 (독립된 두 집단)
# =========================================================
kospi_rate = df[df['시장구분'] == 'KOSPI']['등락률'].dropna()
kosdaq_rate = df[df['시장구분'] == 'KOSDAQ']['등락률'].dropna()

# 중심극한정리(CLT, n >= 30)에 따른 모수적 검정(독립표본 t-검정) 수행
# 등분산 검정
levene_res = stats.levene(kospi_rate, kosdaq_rate)
equal_var = levene_res.pvalue > 0.05
res1 = stats.ttest_ind(kospi_rate, kosdaq_rate, equal_var=equal_var)
t_obs1, p_val1, dof1 = res1.statistic, res1.pvalue, res1.df

print("=" * 65)
print("검정 ① KOSPI와 KOSDAQ의 등락률 비교")
print("귀무가설(H₀): KOSPI와 KOSDAQ 시장 간 등락률의 차이가 없다. (두 시장의 평균 등락률은 같다)")
print("대립가설(H₁): KOSPI와 KOSDAQ 시장 간 등락률의 차이가 있다. (두 시장의 평균 등락률은 다르다)")
print("검정 방법/이유: 독립표본 t-검정 (Independent Two-Sample t-test)")
print(f"  - 표본 크기(KOSPI: {len(kospi_rate)}개, KOSDAQ: {len(kosdaq_rate)}개)가 30보다 충분히 크므로,")
print("    중심극한정리(CLT)에 의해 표본평균의 표집분포가 정규분포를 따르므로 t-검정을 적용함.")
print(f"결과: t-통계량 = {t_obs1:.4f}, p-value = {p_val1:.4f}, 자유도 = {dof1:.1f}")
if p_val1 < 0.05:
    print("해석: 유의수준 0.05에서 p-value < 0.05이므로 귀무가설을 기각한다.")
    print("      따라서 KOSPI와 KOSDAQ 시장 간 등락률에는 통계적으로 유의미한 차이가 있다.")
else:
    print("해석: 유의수준 0.05에서 p-value >= 0.05이므로 귀무가설을 기각하지 못한다.")
    print("      따라서 두 시장 간 등락률에는 유의미한 차이가 있다고 볼 수 없다.")

# 시각화 ①
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# (1) 왼쪽: 두 집단 평균 및 95% 신뢰구간
groups1 = [('KOSPI', kospi_rate, '#1C7ED6'), ('KOSDAQ', kosdaq_rate, '#F03E3E')]
for i, (name, g, color) in enumerate(groups1):
    mean_val = g.mean()
    ci = stats.t.interval(0.95, len(g) - 1, loc=mean_val, scale=stats.sem(g))
    ax1.errorbar(i, mean_val, yerr=[[mean_val - ci[0]], [ci[1] - mean_val]],
                 fmt='o', color=color, markersize=8, capsize=6, linewidth=2)
    ax1.text(i + 0.15, mean_val, f'평균 {mean_val:.2f}%\n(n={len(g)})', va='center', fontsize=10)
ax1.set_xticks([0, 1], [name for name, _, _ in groups1])
ax1.set_xlim(-0.5, 1.8)
ax1.set_ylabel('등락률 (%)')
ax1.set_title(f'KOSPI vs KOSDAQ 평균 등락률 (95% CI)')
ax1.grid(axis='y', alpha=0.3)
ax1.spines[['top', 'right']].set_visible(False)

# (2) 오른쪽: 첨부 이미지 형식의 t-분포, 기각역, p-value 시각화
t_crit1 = stats.t.ppf(0.975, dof1)
lim1 = max(4.0, abs(t_obs1) + 1.2)
x1 = np.linspace(-lim1, lim1, 1000)
y1 = stats.t.pdf(x1, dof1)

ax2.plot(x1, y1, color='#495057', linewidth=2)
ax2.fill_between(x1, y1, where=(np.abs(x1) >= abs(t_obs1)), color='#74C0FC',
                 label=f'p-value = 파랑과 빨강을 합친 넓이 ({p_val1:.3f})')
ax2.fill_between(x1, y1, where=(np.abs(x1) >= t_crit1), color='#E03131',
                 label=f'기각역 (|t| ≥ {t_crit1:.2f}, 합 5%)')
ax2.axvline(t_obs1, color='#1C7ED6', linestyle='--', linewidth=1.8)
pos_text1 = '기각역 안(꼬리)' if abs(t_obs1) >= t_crit1 else '기각역 밖(가운데)'
ax2.text(t_obs1 + 0.1, max(y1) * 0.88, f'관측한 t = {t_obs1:.2f}', color='#1C7ED6', fontsize=11, fontweight='bold')
ax2.set_title(f'자유도 {dof1:.0f}인 t-분포 : 관측한 t가 {pos_text1}에 있음')
ax2.set_xlabel('t 값')
ax2.set_yticks([])
ax2.legend(loc='upper left', frameon=False, fontsize=9.5)
ax2.spines[['top', 'right', 'left']].set_visible(False)

plt.suptitle('검정 ①: KOSPI와 KOSDAQ의 등락률 비교 (독립표본 t-검정)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()


# =========================================================
# 검정 ② 종가와 시가 비교 (대응 표본)
# =========================================================
paired_df = df[['시가', '종가']].dropna()
paired_df = paired_df[(paired_df['시가'] > 0) & (paired_df['종가'] > 0)].copy()

# 대응표본 t-검정 수행 (종가 - 시가)
# n >= 30 이므로 중심극한정리에 의해 대응표본 t-검정 타당
res2 = stats.ttest_rel(paired_df['종가'], paired_df['시가'])
t_obs2, p_val2, dof2 = res2.statistic, res2.pvalue, res2.df

print("\n" + "=" * 65)
print("검정 ② 종가와 시가 비교 (대응 표본)")
print("귀무가설(H₀): 같은 종목의 종가와 시가는 차이가 없다. (장중 가격 변동의 평균은 0이다)")
print("대립가설(H₁): 같은 종목의 종가와 시가는 차이가 있다. (장중 가격 변동의 평균은 0이 아니다)")
print("검정 방법/이유: 대응표본 t-검정 (Paired Samples t-test)")
print(f"  - 표본 크기(n={len(paired_df)})가 30보다 매우 커 중심극한정리(CLT)를 만족하므로,")
print("    종목별 시가와 종가의 차이 평균에 대해 대응표본 t-검정을 적용함.")
print(f"결과: t-통계량 = {t_obs2:.4f}, p-value = {p_val2:.4e}, 자유도 = {dof2}")
if p_val2 < 0.05:
    print("해석: 유의수준 0.05에서 p-value < 0.05이므로 귀무가설을 기각한다.")
    print("      따라서 당일 종가와 시가 사이에는 통계적으로 유의미한 차이가 존재한다.")
else:
    print("해석: 유의수준 0.05에서 p-value >= 0.05이므로 귀무가설을 기각하지 못한다.")
    print("      따라서 종가와 시가 간에 유의미한 차이가 있다고 볼 수 없다.")

# 시각화 ②
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# (1) 왼쪽: 평균 시가 vs 종가
means2 = [paired_df['시가'].mean(), paired_df['종가'].mean()]
stds2 = [paired_df['시가'].std() / np.sqrt(len(paired_df)), paired_df['종가'].std() / np.sqrt(len(paired_df))]
ax1.bar(['시가 (Open)', '종가 (Close)'], means2, yerr=stds2, capsize=6, color=['#74C0FC', '#63E6BE'], edgecolor='gray', width=0.45)
ax1.set_title('전체 종목 평균 시가 vs 종가')
ax1.set_ylabel('가격 (원)')
for idx, m in enumerate(means2):
    ax1.text(idx, m * 0.5, f'{m:,.0f}원', ha='center', va='center', color='black', fontweight='bold', fontsize=11)
ax1.grid(axis='y', alpha=0.3)
ax1.spines[['top', 'right']].set_visible(False)

# (2) 오른쪽: t-분포 시각화 (요청하신 양식)
t_crit2 = stats.t.ppf(0.975, dof2)
lim2 = max(4.0, abs(t_obs2) + 1.2)
x2 = np.linspace(-lim2, lim2, 1000)
y2 = stats.t.pdf(x2, dof2)

ax2.plot(x2, y2, color='#495057', linewidth=2)
ax2.fill_between(x2, y2, where=(np.abs(x2) >= abs(t_obs2)), color='#74C0FC',
                 label=f'p-value = 파랑과 빨강을 합친 넓이 ({p_val2:.3e})')
ax2.fill_between(x2, y2, where=(np.abs(x2) >= t_crit2), color='#E03131',
                 label=f'기각역 (|t| ≥ {t_crit2:.2f}, 합 5%)')
ax2.axvline(t_obs2, color='#1C7ED6', linestyle='--', linewidth=1.8)
pos_text2 = '기각역 안(꼬리)' if abs(t_obs2) >= t_crit2 else '기각역 밖(가운데)'
ax2.text(t_obs2 + 0.1, max(y2) * 0.88, f'관측한 t = {t_obs2:.2f}', color='#1C7ED6', fontsize=11, fontweight='bold')
ax2.set_title(f'자유도 {dof2}인 t-분포 : 관측한 t가 {pos_text2}에 있음')
ax2.set_xlabel('t 값')
ax2.set_yticks([])
ax2.legend(loc='upper right', frameon=False, fontsize=9.5)
ax2.spines[['top', 'right', 'left']].set_visible(False)

plt.suptitle('검정 ②: 같은 종목의 종가와 시가 비교 (대응표본 t-검정)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()


# =========================================================
# 검정 ③ 시장과 상승·하락의 연관성 (범주형 두 변수)
# =========================================================
cat_df = df[df['시장구분'].isin(['KOSPI', 'KOSDAQ'])].copy()
cat_df['등락상태'] = cat_df['등락률'].apply(lambda x: '상승' if x > 0 else ('하락' if x < 0 else None))
cat_filtered = cat_df.dropna(subset=['등락상태']).copy()
ct = pd.crosstab(cat_filtered['시장구분'], cat_filtered['등락상태'])

# 카이제곱 독립성 검정
chi2_stat, chi2_pval, dof3, expected = stats.chi2_contingency(ct)

print("\n" + "=" * 65)
print("검정 ③ 시장과 상승·하락의 연관성")
print("귀무가설(H₀): 시장 구분(KOSPI, KOSDAQ)과 주가 상승·하락 여부는 서로 독립이다. (연관성이 없다)")
print("대립가설(H₁): 시장 구분(KOSPI, KOSDAQ)과 주가 상승·하락 여부는 독립이 아니다. (연관성이 있다)")
print("검정 방법/이유: 카이제곱 독립성 검정 (Chi-square Test of Independence)")
print(f"  - 두 변수 모두 범주형 자료이며, 최소 기대빈도({expected.min():.1f})가 5 이상으로 적합 요건을 충족함.")
print(f"결과: 교차표 (관측 빈도):\n{ct}")
print(f"      카이제곱 통계량(χ²) = {chi2_stat:.4f}, p-value = {chi2_pval:.4f}, 자유도 = {dof3}")
if chi2_pval < 0.05:
    print("해석: 유의수준 0.05에서 p-value < 0.05이므로 귀무가설을 기각한다.")
    print("      따라서 시장 종류(KOSPI, KOSDAQ)와 주가의 상승·하락 간에는 통계적으로 유의미한 연관성이 있다.")
else:
    print("해석: 유의수준 0.05에서 p-value >= 0.05이므로 귀무가설을 기각하지 못한다.")
    print("      따라서 시장 종류와 주가의 상승·하락은 서로 통계적으로 독립이다 (연관성이 없다).")

# 시각화 ③
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

# (1) 왼쪽: 시장별 상승/하락 비율 (수평 누적 막대 그래프, 05번 실습 예제 스타일)
ratio_df = ct.div(ct.sum(axis=1), axis=0) * 100
rows = list(ratio_df.index)
cols = list(ratio_df.columns)
colors_cat = ['#1C7ED6', '#F03E3E']  # 상승: 파랑, 하락: 빨강

left = np.zeros(len(rows))
for j, col_name in enumerate(cols):
    vals = ratio_df[col_name].values
    ax1.barh(rows, vals, left=left, color=colors_cat[j], label=col_name, height=0.55, edgecolor='black', alpha=0.85)
    for i in range(len(rows)):
        count_val = ct.loc[rows[i], col_name]
        ax1.text(left[i] + vals[i] / 2, i, f'{vals[i]:.1f}%\n({count_val}종목)',
                 ha='center', va='center', color='white', fontweight='bold', fontsize=10)
    left += vals

ax1.set_xlim(0, 100)
ax1.set_xlabel('비율 (%)', fontsize=11)
ax1.set_title(f'시장별 상승 / 하락 비율 (p = {chi2_pval:.3f})', fontsize=12)
ax1.legend(title='등락상태', frameon=False, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2)
ax1.invert_yaxis()
ax1.spines[['top', 'right']].set_visible(False)
ax1.grid(axis='x', alpha=0.3)

# (2) 오른쪽: 카이제곱 분포에서 검정통계량 및 기각역 시각화
chi_crit = stats.chi2.ppf(0.95, dof3)
x3 = np.linspace(0.08, max(8.0, chi2_stat + 4.0), 1000)
y3 = stats.chi2.pdf(x3, dof3)

ax2.plot(x3, y3, color='#495057', linewidth=2)
ax2.fill_between(x3, y3, where=(x3 >= chi2_stat), color='#74C0FC',
                 label=f'p-value = 파랑과 빨강을 합친 넓이 ({chi2_pval:.3f})')
ax2.fill_between(x3, y3, where=(x3 >= chi_crit), color='#E03131',
                 label=f'기각역 (χ² ≥ {chi_crit:.2f}, 5%)')
ax2.axvline(chi2_stat, color='#1C7ED6', linestyle='--', linewidth=1.8)
pos_text3 = '기각역 안(꼬리)' if chi2_stat >= chi_crit else '기각역 밖(가운데)'
ax2.text(chi2_stat + 0.15, 0.22, f'관측한 χ² = {chi2_stat:.2f}', color='#1C7ED6', fontsize=11, fontweight='bold')
ax2.set_title(f'자유도 {dof3}인 χ²-분포 : 관측한 χ²이 {pos_text3}에 있음', fontsize=12)
ax2.set_xlabel('χ² 값', fontsize=11)
ax2.set_xlim(0, max(8.0, chi2_stat + 4.0))
ax2.set_ylim(0, 0.35)  # 적절한 높이 설정으로 곡선 왜곡 및 바닥 찌부 방지
ax2.set_yticks([])
ax2.legend(loc='upper right', frameon=False, fontsize=9.5)
ax2.spines[['top', 'right', 'left']].set_visible(False)

plt.suptitle('검정 ③: 시장과 상승·하락의 연관성 (카이제곱 독립성 검정)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.subplots_adjust(bottom=0.22)
plt.show()
