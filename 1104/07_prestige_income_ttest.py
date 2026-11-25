# [11장 실습 1] prestige 데이터 : 블루칼라와 화이트칼라의 평균 소득 차이 t-검정과 결과 시각화
import numpy as np  # 수치 계산 라이브러리
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt  # 그래프 출력용 라이브러리
from matplotlib import font_manager  # 설치된 폰트 확인용
from pathlib import Path

# 귀무가설(H0) : 화이트칼라와 블루칼라 근로자의 평균 소득은 같다.
# 대립가설(H1) : 화이트칼라와 블루칼라 근로자의 평균 소득은 다르다.   (양측 검정, 유의수준 0.05)

# 이 파일의 위치를 기준으로 데이터 폴더를 찾는다(어느 폴더에서 실행해도 동작)
DATA_DIR = Path(__file__).resolve().parents[2] / 'data'
OUT_DIR = Path(__file__).resolve().parent  # 그래프는 이 파일과 같은 폴더에 저장

# 한글 폰트 설정: 설치된 폰트 중 처음 발견되는 것을 사용(윈도우는 Malgun Gothic)
installed = {f.name for f in font_manager.fontManager.ttflist}
FONT = next((n for n in ['Malgun Gothic', 'AppleGothic', 'NanumGothic',
                         'Noto Sans CJK KR', 'Noto Sans CJK JP'] if n in installed), None)
plt.rcParams['font.family'] = FONT
plt.rcParams['axes.unicode_minus'] = False

# 데이터 준비
df = pd.read_csv(DATA_DIR / 'prestige.csv')
df.info()
print(df.head())

group_1 = df.loc[df.type == 'bc', 'income']  # 블루칼라
group_2 = df.loc[df.type == 'wc', 'income']  # 화이트칼라
print(group_1)
print(group_2)

print(group_1.count())  # 그룹별 표본 크기
print(group_2.count())  # 그룹별 표본 크기
print(group_1.mean())  # 그룹별 평균
print(group_2.mean())  # 그룹별 평균

print(stats.shapiro(group_1))  # pvalue 0.222 > 0.05 → 정규성 만족
print(stats.shapiro(group_2))  # pvalue 0.090 > 0.05 → 정규성 만족

print(stats.levene(group_1, group_2))  # pvalue 0.694 > 0.05 → 등분산 만족

result = stats.ttest_ind(group_1, group_2, equal_var=True)
print(result)  # statistic=0.630, pvalue=0.531, df=65.0
# pvalue 0.531 > 0.05 → 귀무가설을 기각할 수 없음 : 두 그룹의 평균 소득에 차이가 있다고 볼 수 없음


# ============================================================
# 결과 시각화 ① : 소득 분포와 평균의 95% 신뢰구간
# ============================================================
fig, ax = plt.subplots(figsize=(6, 5))
rng = np.random.default_rng(0)  # 점이 겹치지 않게 좌우로 살짝 흩뜨리기(지터)
groups = [('블루칼라 (bc)', group_1, '#868E96'), ('화이트칼라 (wc)', group_2, '#1C7ED6')]
for i, (name, g, color) in enumerate(groups):
    x = i + rng.uniform(-0.12, 0.12, len(g))
    ax.scatter(x, g, color=color, alpha=0.45, s=25)  # 직업 하나가 점 하나
    mean = g.mean()
    ci = stats.t.interval(0.95, len(g) - 1, loc=mean, scale=stats.sem(g))  # 평균의 95% 신뢰구간
    ax.errorbar(i + 0.3, mean, yerr=[[mean - ci[0]], [ci[1] - mean]],
                fmt='o', color=color, markersize=9, capsize=6, linewidth=2)
    ax.text(i + 0.38, mean, f'평균 {mean:,.0f}\n(n={len(g)})', va='center', fontsize=10)
    print(f'{name} 평균 {mean:,.0f}, 95% 신뢰구간 {ci[0]:,.0f} ~ {ci[1]:,.0f}')
    # 블루칼라 (bc) 평균 5,374, 95% 신뢰구간 4,765 ~ 5,984
    # 화이트칼라 (wc) 평균 5,052, 95% 신뢰구간 4,212 ~ 5,893  ← 두 구간이 크게 겹침
ax.set_xticks([0, 1], [n for n, _, _ in groups])
ax.set_xlim(-0.5, 1.9)
ax.set_ylabel('평균 소득 (income, 캐나다 달러)')
ax.set_title(f'직업군별 소득 비교 (t = {result.statistic:.2f}, p = {result.pvalue:.3f})')
ax.spines[['top', 'right']].set_visible(False)
plt.tight_layout()
plt.savefig(OUT_DIR / '실전분석1_소득분포.png', dpi=120)
plt.show()


# ============================================================
# 결과 시각화 ② : t-분포 위에서 본 검정 결과
# ============================================================
t_obs, dof = result.statistic, result.df
t_crit = stats.t.ppf(0.975, dof)  # 유의수준 0.05 양측 검정의 임계값
x = np.linspace(-4, 4, 500)
y = stats.t.pdf(x, dof)

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(x, y, color='#495057', linewidth=2)
ax.fill_between(x, y, where=(np.abs(x) >= abs(t_obs)), color='#74C0FC',
                label=f'p-value = 파랑과 빨강을 합친 넓이 ({result.pvalue:.3f})')  # 관측값보다 극단적인 쪽
ax.fill_between(x, y, where=(np.abs(x) >= t_crit), color='#E03131',
                label=f'기각역 (|t| ≥ {t_crit:.2f}, 합 5%)')
ax.axvline(t_obs, color='#1C7ED6', linestyle='--')
ax.text(t_obs + 0.1, 0.36, f'관측한 t = {t_obs:.2f}', color='#1C7ED6', fontsize=11)
ax.set_title(f'자유도 {dof:.0f}인 t-분포 : 관측한 t가 기각역 밖(가운데)에 있음')
ax.set_xlabel('t 값')
ax.set_yticks([])
ax.legend(loc='upper left', frameon=False)
ax.spines[['top', 'right', 'left']].set_visible(False)
plt.tight_layout()
plt.savefig(OUT_DIR / '실전분석1_t분포.png', dpi=120)
plt.show()
print('임계값 :', round(t_crit, 3))  # 1.997
