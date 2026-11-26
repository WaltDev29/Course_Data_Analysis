# [코드 14-5] 고객 데이터 분석 : 서울시 상권 추정매출로 업종별 고객층 분석과 상권 세분화
# 데이터 : 서울 열린데이터광장 → 서울시 상권분석서비스(추정매출-상권) → 연도별 CSV
#          '서울시 상권분석서비스(추정매출-상권)_2025년.csv' 를 data 폴더에 저장
import numpy as np  # 수치 계산 라이브러리
import pandas as pd  # 데이터 처리 라이브러리
import matplotlib.pyplot as plt  # 그래프 출력용 라이브러리
from matplotlib import font_manager  # 설치된 폰트 확인용
import seaborn as sns  # 통계 시각화 라이브러리
from sklearn.preprocessing import StandardScaler  # 표준화
from sklearn.cluster import KMeans  # k-평균 군집화
from sklearn.metrics import silhouette_score, silhouette_samples  # 군집 품질 지표(실루엣 계수)
from sklearn.decomposition import PCA  # 시각화용 2차원 축소
from pathlib import Path  # 파일 경로 처리용

DATA_DIR = Path(__file__).resolve().parents[1] / 'data'
OUT_DIR = Path(__file__).resolve().parent
CSV = DATA_DIR / 'seoul_customer.csv'
QUARTER = 20254  # 분석할 분기 (2025년 4분기)
TARGET = '커피-음료'  # 분석할 업종

# 한글 폰트 설정: 설치된 폰트 중 처음 발견되는 것을 사용(윈도우는 Malgun Gothic)
installed = {f.name for f in font_manager.fontManager.ttflist}
FONT = next((n for n in ['Malgun Gothic', 'AppleGothic', 'NanumGothic',
                         'Noto Sans CJK KR', 'Noto Sans CJK JP'] if n in installed), None)
plt.rcParams['font.family'] = FONT
plt.rcParams['axes.unicode_minus'] = False
pd.set_option('display.width', 200)

AGE_COLS = ['연령대_10_매출_금액', '연령대_20_매출_금액', '연령대_30_매출_금액',
            '연령대_40_매출_금액', '연령대_50_매출_금액', '연령대_60_이상_매출_금액']
AGE_NAMES = ['10대', '20대', '30대', '40대', '50대', '60대 이상']
TIME_COLS = ['시간대_00~06_매출_금액', '시간대_06~11_매출_금액', '시간대_11~14_매출_금액',
             '시간대_14~17_매출_금액', '시간대_17~21_매출_금액', '시간대_21~24_매출_금액']
TIME_NAMES = ['00~06시', '06~11시', '11~14시', '14~17시', '17~21시', '21~24시']
DAY_COLS = ['월요일_매출_금액', '화요일_매출_금액', '수요일_매출_금액', '목요일_매출_금액',
            '금요일_매출_금액', '토요일_매출_금액', '일요일_매출_금액']


def share(data, cols, names):
    """여러 열의 합계를 100으로 하는 비율(%) 데이터프레임"""
    r = data[cols].div(data[cols].sum(axis=1), axis=0) * 100
    r.columns = names
    return r


# ============================================================
# [1] 데이터 읽기
# ============================================================
df = pd.read_csv(CSV, encoding='cp949', low_memory=False)  # 공공데이터 CSV는 cp949
print(df.shape)  # (85732, 55)
print(df.iloc[:3, :9])  # 앞 3행, 식별 열과 전체 매출


# ============================================================
# [2] 데이터 구조 확인
# ============================================================
print(df['기준_년분기_코드'].value_counts().sort_index())  # 20251 21427, 20252 21452, 20253 21520, 20254 21333
print(df['상권_구분_코드_명'].value_counts())  # 골목상권 42995, 발달상권 29074, 전통시장 12680, 관광특구 983
print(df['상권_코드_명'].nunique(), df['서비스_업종_코드_명'].nunique())  # 1577 62
# 한 행 = '분기 × 상권 × 업종' 의 매출. 매출을 요일·시간대·성별·연령대로 나눈 금액과 건수가 열로 들어 있음
print(df.columns[:11].tolist())  # 식별 열 7개 + 당월 매출·건수 + 주중·주말 매출
print([c for c in df.columns if c.startswith('시간대')])  # 금액 6개 + 건수 6개
print([c for c in df.columns if c.startswith('연령대') and c.endswith('금액')])  # 연령대 매출 금액 6개


# ============================================================
# [3] 데이터 품질 점검
# ============================================================
print(df.isna().sum().sum())  # 0 : 결측값 없음
q = df[df['기준_년분기_코드'] == QUARTER].copy()
week_gap = (q['주중_매출_금액'] + q['주말_매출_금액'] - q['당월_매출_금액']).abs().max()
print(week_gap)  # 0 : 주중 + 주말 = 전체 매출로 정확히 일치
sex_sum = q['남성_매출_금액'] + q['여성_매출_금액']
print((sex_sum / q['당월_매출_금액']).describe().round(3))  # 평균 0.922, 중앙값 0.985
# → 성별·연령대 합계는 전체 매출의 평균 92%. 성별을 알 수 없는 매출(법인 카드 등)이 빠져 있음
#   비율의 분모는 '당월 매출'이 아니라 '성별(연령대) 합계'로 함
print([c for c in q.columns if '건수~' in c])  # 시간대 건수 열 이름이 '시간대_건수~06_매출_건수'로 원본부터 불규칙함


# ============================================================
# [4] 서울 전체 매출 개요 : 분기별 매출과 상권 구분별 비중
# ============================================================
by_q = df.groupby('기준_년분기_코드')['당월_매출_금액'].sum() / 1e12  # 조 원
print(by_q.round(2))
by_type = q.groupby('상권_구분_코드_명')['당월_매출_금액'].sum()
print((by_type / by_type.sum() * 100).round(1).sort_values(ascending=False))

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].bar([f'{c % 10}분기' for c in by_q.index], by_q.values, color='#4472C4')
for i, v in enumerate(by_q.values):
    axes[0].text(i, v, f'{v:.1f}', ha='center', va='bottom')
axes[0].set_title('2025년 분기별 추정 매출 (조 원)')
type_share = (by_type / by_type.sum() * 100).sort_values()
axes[1].barh(type_share.index, type_share.values, color='#4472C4')
for i, v in enumerate(type_share.values):
    axes[1].text(v, i, f' {v:.1f}%', va='center')
axes[1].set_title(f'상권 구분별 매출 비중 ({QUARTER // 10}년 {QUARTER % 10}분기)')
for ax in axes:
    ax.spines[['top', 'right']].set_visible(False)
plt.tight_layout()
plt.savefig(OUT_DIR / '14주_0_매출개요.png', dpi=150)
plt.show()


# ============================================================
# [4-2] 상권별 매출 규모 : 매출 상위 상권과 분포
# ============================================================
area = q.groupby(['상권_코드_명', '상권_구분_코드_명'])['당월_매출_금액'].agg(['sum', 'count'])
area['sum'] = area['sum'] / 1e8  # 억 원, count : 상권 안의 업종 수
print(area.nlargest(10, 'sum').round(0))  # 노량진역 12616억, 가산디지털단지 8044억, 용산전자상가 6690억 ...
area_sales = q.groupby('상권_코드_명')['당월_매출_금액'].sum() / 1e8
print(area_sales.describe().round(1))  # 1565개 상권, 평균 156.1억, 중앙값 34.3억
top_share = area_sales.nlargest(len(area_sales) // 10).sum() / area_sales.sum() * 100
print(round(top_share, 1))  # 67.2 : 상위 10% 상권이 매출의 2/3를 차지
# → 평균(156.1억)이 중앙값(34.3억)의 4배 이상. 소수의 대형 상권이 평균을 끌어올림


# ============================================================
# [5] 업종별 주 고객층 : 매출 상위 10개 업종의 연령대·시간대 비율
# ============================================================
by_ind = q.groupby('서비스_업종_코드_명')[AGE_COLS + TIME_COLS + ['당월_매출_금액']].sum()
top10 = by_ind.nlargest(10, '당월_매출_금액')
print((top10['당월_매출_금액'] / 1e8).round(0))  # 억 원 : 한식음식점 39859, 일반의류 21322, 일반의원 17877 ...

age_share = share(top10, AGE_COLS, AGE_NAMES).round(1)
time_share = share(top10, TIME_COLS, TIME_NAMES).round(1)
print(age_share)
print(time_share)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
sns.heatmap(age_share, annot=True, fmt='.1f', cmap='Blues', ax=axes[0], cbar=False)
axes[0].set_title('업종별 연령대 매출 비율 (%, 행 합계 100)')
sns.heatmap(time_share, annot=True, fmt='.1f', cmap='Oranges', ax=axes[1], cbar=False)
axes[1].set_title('업종별 시간대 매출 비율 (%, 행 합계 100)')
for ax in axes:
    ax.set_ylabel('')
axes[1].set_yticklabels([])
plt.suptitle(f'서울시 매출 상위 10개 업종의 고객층 ({QUARTER // 10}년 {QUARTER % 10}분기)', fontsize=14)
plt.tight_layout()
plt.savefig(OUT_DIR / '14주_1_업종별고객층.png', dpi=150)
plt.show()


# ============================================================
# [5-2] 이상값 확인 : 반찬가게의 00~06시 비율 16.7%는 어디서 왔나
# ============================================================
side = q[q['서비스_업종_코드_명'] == '반찬가게'].copy()
side.index = side['상권_코드_명']
side['00~06시 비율'] = side['시간대_00~06_매출_금액'] / side[TIME_COLS].sum(axis=1) * 100
side['매출(억)'] = side['당월_매출_금액'] / 1e8
print(len(side), '개 상권')  # 400 개 상권
print(side.nlargest(5, '시간대_00~06_매출_금액')[['상권_구분_코드_명', '매출(억)', '00~06시 비율']].round(1))
# 가락시장 3062.2억 · 41.4%, 방이역 1번 50.2억 · 61.0%, 장평중학교 199.3억 · 14.4% ...
night_top5 = side.nlargest(5, '시간대_00~06_매출_금액')['시간대_00~06_매출_금액'].sum()
print(round(night_top5 / side['시간대_00~06_매출_금액'].sum() * 100, 1))  # 95.3 : 상위 5개 상권이 심야 매출의 95.3%
print(side['00~06시 비율'].median())  # 0.0 : 보통의 반찬가게는 심야 매출이 없음
# → 도매시장(가락시장)의 새벽 거래가 업종 전체 비율을 끌어올린 것. 합계 비율은 큰 상권 몇 곳에 좌우될 수 있음


# ============================================================
# [6] 업종별 여성 비율 · 주말 비율 · 객단가 (매출 상위 20개 업종)
# ============================================================
cols = ['남성_매출_금액', '여성_매출_금액', '주말_매출_금액', '당월_매출_금액', '당월_매출_건수']
ind = q.groupby('서비스_업종_코드_명')[cols].sum().nlargest(20, '당월_매출_금액')
ind['여성 비율'] = ind['여성_매출_금액'] / (ind['남성_매출_금액'] + ind['여성_매출_금액']) * 100
ind['주말 비율'] = ind['주말_매출_금액'] / ind['당월_매출_금액'] * 100
ind['객단가(천원)'] = ind['당월_매출_금액'] / ind['당월_매출_건수'] / 1000
print(ind[['여성 비율', '주말 비율', '객단가(천원)']].round(1).sort_values('여성 비율'))

fig, axes = plt.subplots(1, 3, figsize=(16, 6), sharey=False)
for ax, col, color in zip(axes, ['여성 비율', '주말 비율', '객단가(천원)'], ['#C0504D', '#4472C4', '#9BBB59']):
    s = ind[col].sort_values()
    ax.barh(s.index, s.values, color=color)
    for i, v in enumerate(s.values):
        ax.text(v, i, f' {v:.1f}', va='center', fontsize=8)
    if col != '객단가(천원)':
        ax.axvline(50 if col == '여성 비율' else 2 / 7 * 100, color='gray', linestyle='--', linewidth=1)
    ax.set_title(col)
    ax.spines[['top', 'right']].set_visible(False)
    ax.tick_params(axis='y', labelsize=9)
plt.suptitle('매출 상위 20개 업종 비교 (점선 : 여성 50%, 주말 2/7 = 28.6%)', fontsize=13)
plt.tight_layout()
plt.savefig(OUT_DIR / '14주_1b_업종비교.png', dpi=150)
plt.show()


# ============================================================
# [7] 한 업종의 고객 프로필 : 커피-음료
# ============================================================
cafe_all = q[q['서비스_업종_코드_명'] == TARGET].copy()
print(len(cafe_all), '개 상권')  # 1069 개 상권
total = cafe_all[AGE_COLS + TIME_COLS + DAY_COLS + ['남성_매출_금액', '여성_매출_금액',
                                                     '당월_매출_금액', '당월_매출_건수']].sum()
print('객단가 :', round(total['당월_매출_금액'] / total['당월_매출_건수']), '원')  # 1건당 평균 결제 금액 : 8225 원
print('여성 비율 :', round(total['여성_매출_금액'] / (total['남성_매출_금액'] + total['여성_매출_금액']) * 100, 1))

# 커피-음료 매출 상위 10개 상권
top_cafe = pd.DataFrame({'구분': cafe_all['상권_구분_코드_명'].values,
                         '매출(억)': cafe_all['당월_매출_금액'].values / 1e8,
                         '객단가': (cafe_all['당월_매출_금액'] / cafe_all['당월_매출_건수']).values,
                         '여성 비율': (cafe_all['여성_매출_금액'] / (cafe_all['남성_매출_금액'] + cafe_all['여성_매출_금액']) * 100).values,
                         '주말 비율': (cafe_all['주말_매출_금액'] / cafe_all['당월_매출_금액'] * 100).values},
                        index=cafe_all['상권_코드_명'])
print(top_cafe.nlargest(10, '매출(억)').round(1))
# 명동 남대문 일대 235.5억, 강남역 137.9억, 여의도역 134.4억(주말 6.2%), 시청역_8번 122.6억(여성 31.6%, 주말 7.3%) ...

fig, axes = plt.subplots(1, 3, figsize=(15, 4.2))
for ax, cols_, names, title in [(axes[0], AGE_COLS, AGE_NAMES, '연령대'),
                                (axes[1], TIME_COLS, TIME_NAMES, '시간대'),
                                (axes[2], DAY_COLS, list('월화수목금토일'), '요일')]:
    s = total[cols_] / total[cols_].sum() * 100
    bars = ax.bar(names, s.values, color='#4472C4')
    for b, v in zip(bars, s.values):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.5, f'{v:.1f}', ha='center', fontsize=9)
    ax.set_title(f'{title}별 매출 비율 (%)')
    ax.spines[['top', 'right']].set_visible(False)
    ax.tick_params(axis='x', rotation=30)
plt.suptitle(f'서울 {TARGET} 업종의 고객 프로필', fontsize=14)
plt.tight_layout()
plt.savefig(OUT_DIR / '14주_2_커피고객프로필.png', dpi=150)
plt.show()


# ============================================================
# [8] 커피-음료 : 상권 구분별 고객층 비교
# ============================================================
by_area = cafe_all.groupby('상권_구분_코드_명')[AGE_COLS + TIME_COLS + ['주말_매출_금액', '당월_매출_금액']].sum()
area_age = share(by_area, AGE_COLS, AGE_NAMES).round(1)
area_time = share(by_area, TIME_COLS, TIME_NAMES).round(1)
area_age['주말 비율'] = (by_area['주말_매출_금액'] / by_area['당월_매출_금액'] * 100).round(1)
print(area_age)
print(area_time)
by_day = cafe_all.groupby('상권_구분_코드_명')[DAY_COLS].sum()
area_day = share(by_day, DAY_COLS, list('월화수목금토일')).round(1)
print(area_day)  # 발달상권 수 17.0 · 일 10.4, 전통시장 토 16.3 · 골목상권 토 15.7 (토요일이 수요일과 같거나 큼)

fig, axes = plt.subplots(1, 2, figsize=(14, 3.6))
sns.heatmap(area_age.drop(columns='주말 비율'), annot=True, fmt='.1f', cmap='Blues', ax=axes[0], cbar=False)
axes[0].set_title('상권 구분별 연령대 비율 (%)')
sns.heatmap(area_time, annot=True, fmt='.1f', cmap='Oranges', ax=axes[1], cbar=False)
axes[1].set_title('상권 구분별 시간대 비율 (%)')
axes[1].set_yticklabels([])
for ax in axes:
    ax.set_ylabel('')
plt.suptitle(f'{TARGET} : 상권 구분에 따른 고객층 차이', fontsize=13)
plt.tight_layout()
plt.savefig(OUT_DIR / '14주_2b_상권구분비교.png', dpi=150)
plt.show()


# ============================================================
# [9] 커피-음료 : 분기별 변화
# ============================================================
cafe_year = df[df['서비스_업종_코드_명'] == TARGET]
by_q2 = cafe_year.groupby('기준_년분기_코드')[TIME_COLS + ['당월_매출_금액', '당월_매출_건수']].sum()
qt = share(by_q2, TIME_COLS, TIME_NAMES).round(1)
qt['매출(억)'] = (by_q2['당월_매출_금액'] / 1e8).round(0)
qt['객단가'] = (by_q2['당월_매출_금액'] / by_q2['당월_매출_건수']).round(0)
print(qt)

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].bar([f'{c % 10}분기' for c in qt.index], qt['매출(억)'], color='#4472C4')
for i, v in enumerate(qt['매출(억)']):
    axes[0].text(i, v, f'{v:,.0f}', ha='center', va='bottom')
axes[0].set_title(f'{TARGET} 분기별 매출 (억 원)')
for t in ['06~11시', '11~14시', '14~17시', '17~21시']:
    axes[1].plot([f'{c % 10}분기' for c in qt.index], qt[t], marker='o', label=t)
axes[1].set_title('분기별 시간대 매출 비율 (%)')
axes[1].legend(frameon=False, ncol=2)
for ax in axes:
    ax.spines[['top', 'right']].set_visible(False)
plt.tight_layout()
plt.savefig(OUT_DIR / '14주_2c_분기변화.png', dpi=150)
plt.show()


# ============================================================
# [10] 상권 세분화 ① 지표 만들기
# ============================================================
cafe = cafe_all[cafe_all['당월_매출_건수'] >= 1000].copy()  # 건수가 너무 적은 상권은 비율이 불안정하므로 제외
cafe.index = cafe['상권_코드_명']
print(len(cafe), '개 상권')  # 986 개 상권

A = share(cafe, AGE_COLS, AGE_NAMES)[['20대', '30대', '40대', '50대', '60대 이상']]  # 10대는 매우 작아 제외
T = share(cafe, TIME_COLS, TIME_NAMES)[['06~11시', '11~14시', '14~17시', '17~21시', '21~24시']]  # 심야 제외
E = pd.DataFrame({'여성 비율': cafe['여성_매출_금액'] / (cafe['남성_매출_금액'] + cafe['여성_매출_금액']) * 100,
                  '주말 비율': cafe['주말_매출_금액'] / cafe['당월_매출_금액'] * 100})
X = pd.concat([A, T, E], axis=1)  # 상권마다 고객층 지표 12개
print(X.head(3).round(1))
print(X.describe().round(1).T[['mean', 'std', 'min', 'max']])
Z = StandardScaler().fit_transform(X)


# ============================================================
# [11] 상권 세분화 ② 군집 수 정하기 : 엘보와 실루엣 계수
# ============================================================
ks, inertias, sils = range(2, 8), [], []
for k in ks:
    m = KMeans(n_clusters=k, n_init=10, random_state=0).fit(Z)
    inertias.append(m.inertia_)
    sils.append(silhouette_score(Z, m.labels_))
    print(k, round(m.inertia_), round(sils[-1], 3), np.bincount(m.labels_))
# 2 9576 0.217 / 3 8151 0.188 / 4 7561 0.164 / 5 7031 0.168 ...
# 실루엣은 k=2가 가장 높지만 '많다·적다' 정도로만 나뉨 → 해석 가능한 k=4 선택

fig, axes = plt.subplots(1, 2, figsize=(11, 3.8))
axes[0].plot(list(ks), inertias, marker='o', color='#4472C4')
axes[0].set_title('엘보 : 군집 내 거리 제곱합(inertia)')
axes[1].plot(list(ks), sils, marker='o', color='#C0504D')
axes[1].set_title('실루엣 계수 (클수록 군집이 잘 구분됨)')
for ax in axes:
    ax.set_xlabel('군집 수 k')
    ax.axvline(4, color='gray', linestyle='--', linewidth=1)
    ax.spines[['top', 'right']].set_visible(False)
plt.tight_layout()
plt.savefig(OUT_DIR / '14주_2d_군집수.png', dpi=150)
plt.show()


# ============================================================
# [12] 상권 세분화 ③ k-평균과 군집 프로필
# ============================================================
km = KMeans(n_clusters=4, n_init=10, random_state=0).fit(Z)
X['군집'] = km.labels_
profile = X.groupby('군집').mean().round(1)  # 군집별 평균(프로필)
print(profile.T)
print(X['군집'].value_counts().sort_index())  # 413, 241, 216, 116 (군집 번호 순서는 환경에 따라 다를 수 있음)

# 군집 이름 붙이기 : profile 표의 특징으로 정함 (군집 번호는 실행 환경에 따라 바뀔 수 있으므로 규칙으로 지정)
names = {}
names[profile['주말 비율'].idxmin()] = '직장인 점심형'  # 주말 비율이 가장 낮고 11~14시 비율이 높음
names[profile['20대'].idxmax()] = '청년 오후·저녁형'  # 20대·여성·17~21시 비율이 높음
names[profile['60대 이상'].idxmax()] = '장년 동네형'  # 50대·60대 이상 비율이 높음
names[[c for c in profile.index if c not in names][0]] = '일상 복합형'  # 나머지 : 연령·시간대가 고르게 분포, 주말 이용도 많음
names = {int(k): v for k, v in sorted(names.items())}
print(names)
X['유형'] = X['군집'].map(names)
order = ['직장인 점심형', '청년 오후·저녁형', '일상 복합형', '장년 동네형']

# 군집별 대표 상권 : 군집 중심에 가까운 절반 중에서 매출이 큰 3곳
X['매출(억)'] = cafe['당월_매출_금액'] / 1e8
X['중심거리'] = np.linalg.norm(Z - km.cluster_centers_[km.labels_], axis=1)
for c, name in names.items():
    part = X[X['군집'] == c]
    near = part[part['중심거리'] <= part['중심거리'].median()]
    print(name, ':', ', '.join(near.nlargest(3, '매출(억)').index))
# 일상 복합형 : 잠실역, 종로·청계 관광특구, 잠실새내역(신천)
# 청년 오후·저녁형 : 강남역, 홍대입구역(홍대), 명동(명동거리)
# 직장인 점심형 : 명동 남대문 북창동 다동 무교동 관광특구, 여의도역(여의도), 가산디지털단지
# 장년 동네형 : 인사동, 고속터미널(고속터미널역), 미아역

# 군집 품질 확인 : 상권별 실루엣 값을 유형별로 요약
X['실루엣'] = silhouette_samples(Z, km.labels_)
sil = X.groupby('유형')['실루엣'].agg(['mean', 'min', 'max']).loc[order]
sil['음수 비율(%)'] = X.groupby('유형')['실루엣'].apply(lambda v: (v < 0).mean() * 100).loc[order]
print(sil.round(3))
# 직장인 점심형 0.141 / 청년 오후·저녁형 0.126 / 일상 복합형 0.236 / 장년 동네형 0.026 (음수 43.1%)
# → 장년 동네형은 다른 유형과의 경계에 있는 상권이 많음. 유형 안에서도 확신도가 다름

# k = 3으로 나누면 : 군집 프로필을 k = 4와 비교하고, k = 4의 유형이 어떻게 합쳐지는지 확인
k3 = KMeans(n_clusters=3, n_init=10, random_state=0).fit_predict(Z)
profile3 = X.iloc[:, :12].groupby(k3).mean().round(1)  # 12개 지표만 사용
print(profile3.T)
print(np.bincount(k3))  # [276 255 455]
print(pd.crosstab(k3, X['유형'], rownames=['k=3 군집'])[order])
print(pd.crosstab(k3, X['유형'], rownames=['k=3 군집'], margins=True, margins_name='합계')[order + ['합계']])  # 행 합계 = k=3 군집 크기, 열 합계 = k=4 유형 크기
# k=3의 군집 0 ≈ 직장인 점심형, 군집 1 ≈ 청년 오후·저녁형
# 군집 2(455곳) = 일상 복합형 339곳 + 장년 동네형 116곳 → 60대 이상 19.4% (전체 평균 13.9%보다 높지만 장년 동네형 32.6%보다 크게 낮음)
# → k = 3에서는 장년층 상권이 평균적인 상권과 섞여 특징이 약해짐

# 군집 프로필 히트맵 : 전체 평균보다 높으면 빨강, 낮으면 파랑(표준화 값)
zprof = pd.DataFrame(Z, columns=X.columns[:12], index=X.index).groupby(X['유형']).mean()
plt.figure(figsize=(12, 3.8))
sns.heatmap(zprof.loc[order], annot=profile.set_index(profile.index.map(names)).loc[order],
            fmt='.1f', cmap='RdBu_r', center=0, vmin=-1.5, vmax=1.5, cbar_kws={'label': '표준화 값'})
plt.title('커피-음료 상권 유형별 고객층 (칸 안 숫자는 실제 비율 %)')
plt.ylabel('')
plt.tight_layout()
plt.savefig(OUT_DIR / '14주_3_상권유형프로필.png', dpi=150)
plt.show()


# ============================================================
# [13] 상권 세분화 ④ 유형과 상권 구분의 관계, 2차원 시각화
# ============================================================
X['상권 구분'] = cafe['상권_구분_코드_명']
ct = pd.crosstab(X['유형'], X['상권 구분']).loc[order]
print(ct)
print((pd.crosstab(X['유형'], X['상권 구분'], normalize='columns') * 100).round(1).loc[order])

pca = PCA(n_components=2).fit(Z)
P = pca.transform(Z)
plt.figure(figsize=(8, 6))
sns.scatterplot(x=P[:, 0], y=P[:, 1], hue=X['유형'], hue_order=order, s=20, palette='Set2')
plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%})')
plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%})')
plt.title(f'커피-음료 {len(X)}개 상권의 고객층 유형')
plt.tight_layout()
plt.savefig(OUT_DIR / '14주_4_상권유형PCA.png', dpi=150)
plt.show()


# ============================================================
# [14] 다른 분기에서도 유형이 유지되는가 : 2025년 1분기로 같은 분석
# ============================================================
def segment(quarter):
    """한 분기의 커피-음료 상권을 [10]~[12]와 같은 방법으로 4개 유형으로 나눔"""
    c = df[(df['기준_년분기_코드'] == quarter) & (df['서비스_업종_코드_명'] == TARGET)
           & (df['당월_매출_건수'] >= 1000)].copy()
    c.index = c['상권_코드_명']
    Xq = pd.concat([share(c, AGE_COLS, AGE_NAMES)[['20대', '30대', '40대', '50대', '60대 이상']],
                    share(c, TIME_COLS, TIME_NAMES)[['06~11시', '11~14시', '14~17시', '17~21시', '21~24시']],
                    pd.DataFrame({'여성 비율': c['여성_매출_금액'] / (c['남성_매출_금액'] + c['여성_매출_금액']) * 100,
                                  '주말 비율': c['주말_매출_금액'] / c['당월_매출_금액'] * 100})], axis=1)
    lab = KMeans(n_clusters=4, n_init=10, random_state=0).fit_predict(StandardScaler().fit_transform(Xq))
    prof = Xq.groupby(lab).mean()
    nm = {prof['주말 비율'].idxmin(): '직장인 점심형', prof['20대'].idxmax(): '청년 오후·저녁형',
          prof['60대 이상'].idxmax(): '장년 동네형'}
    nm[[k for k in prof.index if k not in nm][0]] = '일상 복합형'
    return Xq, pd.Series(lab, index=Xq.index).map(nm)


X1, type1 = segment(20251)
print(len(X1), '개 상권')  # 998 개 상권
print(X1.groupby(type1).mean().loc[order, ['20대', '60대 이상', '11~14시', '17~21시', '여성 비율', '주말 비율']].round(1))
# 1분기에도 4분기와 같은 특징의 네 유형이 나타남 (직장인 점심형 11~14시 46.8%, 장년 동네형 60대 이상 32.5% ...)

common = X.index.intersection(X1.index)
print(len(common), '개 상권')  # 959 개 상권 : 두 분기 모두 분석 대상
move = pd.crosstab(X.loc[common, '유형'], type1[common], rownames=['4분기'], colnames=['1분기']).loc[order, order]
print(move)
print(round((X.loc[common, '유형'] == type1[common]).mean() * 100, 1))  # 81.1 : 81.1% 상권이 같은 유형
print((np.diag(move) / move.sum(axis=1) * 100).round(1))  # 직장인 87.1, 청년 79.9, 일상 84.7, 장년 59.5
# → 유형은 분기가 바뀌어도 대체로 유지됨. 실루엣이 낮았던 장년 동네형이 가장 많이 바뀜(주로 일상 복합형으로)
