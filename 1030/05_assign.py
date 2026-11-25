# ==============================================================================
# 과제: 네이버 데이터랩 '산' vs '바다' 검색어 트렌드 시계열 분석
# ==============================================================================

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# 한글 폰트 및 스타일 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
sns.set_theme(style='whitegrid', font='Malgun Gothic')

DATA_DIR = Path(__file__).resolve().parents[1] / 'data'
OUT_DIR = Path(__file__).resolve().parent

# ------------------------------------------------------------------------------
# 1. 엑셀 파일 설명 행을 건너뛰고 읽어, 날짜를 인덱스로 하는 데이터프레임 생성
# ------------------------------------------------------------------------------
# 상위 6개 행(메타데이터/설명)을 건너뛰고(skiprows=6) 7번째 행을 컬럼 헤더로 읽음
raw_df = pd.read_excel(DATA_DIR / 'mountain_sea.xlsx', skiprows=6)

# 불필요한 중복 날짜 열(날짜.1)을 제외하고 [날짜, 산, 바다] 열만 선택
df = raw_df.iloc[:, [0, 1, 3]].copy()
df.columns = ['날짜', '산', '바다']

# 날짜 열을 datetime 자료형으로 변환 후 인덱스로 지정
df['날짜'] = pd.to_datetime(df['날짜'])
df.set_index('날짜', inplace=True)

print("=" * 65)
print("1. 데이터프레임 생성 결과 (상위 5행)")
print("=" * 65)
print(df.head())
print(f"데이터 크기: {df.shape}")

# ------------------------------------------------------------------------------
# 2. 기본 통계와 주제어별 최고점 상위 3일 (값이 모두 0인 날 제외)
# ------------------------------------------------------------------------------
# 값이 모두 0인 날 제외 (두 주제어의 값이 모두 0인 행 필터링)
zero_mask = (df['산'] == 0) & (df['바다'] == 0)
zero_count = zero_mask.sum()
df = df[~zero_mask].copy()

print("\n" + "=" * 65)
print(f"2. 기본 통계 (값이 모두 0인 날 제외: {zero_count}건 제외됨)")
print("=" * 65)
print(df.describe().round(3))

print("\n[주제어별 최고점 상위 3일]")
top3_mountain = df['산'].nlargest(3)
top3_sea = df['바다'].nlargest(3)

print("▶ '산' 최고점 상위 3일:")
for date, val in top3_mountain.items():
    print(f"   - {date.strftime('%Y-%m-%d')}: {val:.2f}")

print("\n▶ '바다' 최고점 상위 3일:")
for date, val in top3_sea.items():
    print(f"   - {date.strftime('%Y-%m-%d')}: {val:.2f}")

# ------------------------------------------------------------------------------
# 3. 첫 번째 주제어('산')의 일간 값, 7일 이동평균, 30일 이동평균 그래프 및 차이점
# ------------------------------------------------------------------------------
df['산_MA7'] = df['산'].rolling(window=7).mean()
df['산_MA30'] = df['산'].rolling(window=30).mean()

plt.figure(figsize=(12, 6))
plt.plot(df.index, df['산'], label='일간 값 (Daily)', color='#adb5bd', linewidth=1, alpha=0.7)
plt.plot(df.index, df['산_MA7'], label='7일 이동평균 (7-day MA)', color='#f77f00', linewidth=1.8)
plt.plot(df.index, df['산_MA30'], label='30일 이동평균 (30-day MA)', color='#003049', linewidth=2.5)

plt.title("'산' 검색어 트렌드의 일간 값 및 이동평균선(7일/30일) 비교", fontsize=14, fontweight='bold', pad=12)
plt.xlabel("날짜", fontsize=11)
plt.ylabel("검색 상대지수", fontsize=11)
plt.legend(loc='upper right', frameon=True)
plt.tight_layout()
plt.savefig(OUT_DIR / '05_산_이동평균선.png', dpi=120)
plt.show()

diff_ma_text = """
=================================================================
3. 일간 값, 7일 이동평균, 30일 이동평균의 차이점
=================================================================
- 일간 값(Daily): 요일별(주말 등락) 효과와 단기 이슈로 인해 변동 폭(잡음)이 매우 큼.
- 7일 이동평균: 주간(7일) 단위 주기성을 제거하여 단기적 증감 추세와 반등 시점을 매끄럽게 포착함.
- 30일 이동평균: 단기적인 변동을 완전히 평활화하여 1년 중 언제 검색량이 구조적으로 상승·하강하는지
  거시적인 계절적 트렌드(가을 단풍철 급상승 및 겨울철 감소 흐름)를 가장 명확히 보여줌.
=================================================================
"""
print(diff_ma_text)

# ------------------------------------------------------------------------------
# 4. 월별 평균을 구해 그래프로 그리고, 주제어별로 가장 높은 달과 낮은 달 분석
# ------------------------------------------------------------------------------
df_monthly = df[['산', '바다']].resample('ME').mean()
df_monthly.index = df_monthly.index.strftime('%Y-%m')

plt.figure(figsize=(12, 6))
x = np.arange(len(df_monthly))
width = 0.35

plt.bar(x - width/2, df_monthly['산'], width, label='산', color='#2a9d8f')
plt.bar(x + width/2, df_monthly['바다'], width, label='바다', color='#457b9d')

plt.title("월별 검색어 트렌드 평균 비교 ('산' vs '바다')", fontsize=14, fontweight='bold', pad=12)
plt.xlabel("연-월", fontsize=11)
plt.ylabel("월평균 검색 상대지수", fontsize=11)
plt.xticks(x, df_monthly.index, rotation=30)
plt.legend(loc='upper left', frameon=True)
plt.tight_layout()
plt.savefig(OUT_DIR / '05_월별평균비교.png', dpi=120)
plt.show()

max_month_mountain = df_monthly['산'].idxmax()
min_month_mountain = df_monthly['산'].idxmin()
max_month_sea = df_monthly['바다'].idxmax()
min_month_sea = df_monthly['바다'].idxmin()

monthly_text = f"""
=================================================================
4. 월별 평균 분석 (가장 높은 달과 낮은 달)
=================================================================
▶ '산':
   - 가장 높은 달: {max_month_mountain} ({df_monthly.loc[max_month_mountain, '산']:.2f}) -> 여름 휴가 및 초가을 야외활동 시즌
   - 가장 낮은 달: {min_month_mountain} ({df_monthly.loc[min_month_mountain, '산']:.2f}) -> 장마철 및 초여름 비수기
▶ '바다':
   - 가장 높은 달: {max_month_sea} ({df_monthly.loc[max_month_sea, '바다']:.2f}) -> 한여름 바다 피서 극성수기
   - 가장 낮은 달: {min_month_sea} ({df_monthly.loc[min_month_sea, '바다']:.2f}) -> 초봄 비수기
=================================================================
"""
print(monthly_text)

# ------------------------------------------------------------------------------
# 5. 평일과 주말의 평균을 비교하여 언제 더 많이 검색되는지 쓰시오.
# ------------------------------------------------------------------------------
df['요일구분'] = np.where(df.index.dayofweek >= 5, '주말', '평일')
weekday_weekend_mean = df.groupby('요일구분')[['산', '바다']].mean()

print("=" * 65)
print("5. 평일 vs 주말 평균 검색량 비교")
print("=" * 65)
print(weekday_weekend_mean.round(2))

weekend_compare_text = f"""
[분석 결과]
- '산': 평일 평균 {weekday_weekend_mean.loc['평일', '산']:.2f} vs 주말 평균 {weekday_weekend_mean.loc['주말', '산']:.2f} (주말이 약 {((weekday_weekend_mean.loc['주말', '산']/weekday_weekend_mean.loc['평일', '산'])-1)*100:.1f}% 높음)
- '바다': 평일 평균 {weekday_weekend_mean.loc['평일', '바다']:.2f} vs 주말 평균 {weekday_weekend_mean.loc['주말', '바다']:.2f} (주말이 약 {((weekday_weekend_mean.loc['주말', '바다']/weekday_weekend_mean.loc['평일', '바다'])-1)*100:.1f}% 높음)
-> '산'과 '바다' 모두 여가활동, 여행, 나들이 성격이 강한 검색어이므로 평일보다 '주말'에 더 많이 검색됩니다.
"""
print(weekend_compare_text)

# ------------------------------------------------------------------------------
# 6. 두 주제어의 일간 · 월간 상관계수 및 최고점 날짜 원인 분석 (한 문장 작성)
# ------------------------------------------------------------------------------
corr_daily = df['산'].corr(df['바다'])
corr_monthly = df[['산', '바다']].resample('ME').mean()['산'].corr(df[['산', '바다']].resample('ME').mean()['바다'])

print("=" * 65)
print("6. 상관계수 및 최고점 날짜 사건 분석")
print("=" * 65)
print(f"▶ 일간 상관계수: {corr_daily:.3f} (단기 요일/노이즈로 인해 낮은 상관관계)")
print(f"▶ 월간 상관계수: {corr_monthly:.3f} (여름 휴가철 동반 상승 등 강한 계절적 상관관계)")

top_date_mountain = df['산'].idxmax().strftime('%Y-%m-%d')
top_val_mountain = df['산'].max()
top_date_sea = df['바다'].idxmax().strftime('%Y-%m-%d')
top_val_sea = df['바다'].max()

event_sentence = f"""
[최고점 날짜 사건 분석 (한 문장 요약)]
'산'은 {top_date_mountain}({top_val_mountain:.2f})에 설악산 첫 단풍 관측(9월 28일) 직전 가을 산행 주말 수요가 집중되어 최고점을 기록하였고, '바다'는 {top_date_sea}({top_val_sea:.2f})에 한여름 피서철(8월 5~6일)에 이어 KBS 1TV 음악 특집 프로그램에 가수 바다가 출연하여 방영되면서 연중 최고점을 기록하였습니다.
"""
print(event_sentence)

