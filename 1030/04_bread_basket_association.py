# 빵집 영수증 데이터로 본인 조건(월·평일/주말)의 구매 패턴을 찾는 실습 2 모범 답안
# 데이터 : data 폴더의 bread_basket.csv (영국 에든버러 빵집 'The Bread Basket' 판매 기록)
#          2016-10-30 ~ 2017-04-09, 20,507행
# 본인 조건 : 학번 끝자리로 정한다
#   월   : 0·1 → 2016-11, 2·3 → 2016-12, 4·5 → 2017-01, 6·7 → 2017-02, 8·9 → 2017-03
#   요일 : 끝자리 짝수 → weekday(평일), 홀수 → weekend(주말)
# 실습전 라이브러리 설치
# pip install mlxtend seaborn

import pandas as pd  # 데이터 처리 라이브러리
import seaborn as sns  # 통계 시각화 라이브러리
import matplotlib.pyplot as plt  # 그래프 출력용 라이브러리
from matplotlib import font_manager  # 설치된 폰트 확인용
from mlxtend.frequent_patterns import association_rules, apriori  # 연관규칙 생성, 빈발 항목집합 탐색
from mlxtend.preprocessing import TransactionEncoder  # 영수증별 상품 목록을 True/False 표로 변환
from pathlib import Path  # 파일 경로 처리용

# 이 파일의 위치를 기준으로 데이터 폴더를 찾는다(어느 폴더에서 실행해도 동작)
DATA_DIR = Path(__file__).resolve().parents[1] / 'data'
OUT_DIR = Path(__file__).resolve().parent  # 그래프는 이 파일과 같은 폴더에 저장

MONTH = '2016-12'  # 본인 조건 : 월 (학번 끝자리 6 또는 7)
DAY_TYPE = 'weekend'  # 본인 조건 : weekday(평일) 또는 weekend(주말) (끝자리 7 → 홀수 → 주말)
MIN_SUPPORT = 0.02  # 최소 지지도 : 영수증의 2% 이상에 등장하는 조합만

# 한글 폰트 설정: 설치된 폰트 중 처음 발견되는 것을 사용(윈도우는 Malgun Gothic)
installed = {f.name for f in font_manager.fontManager.ttflist}
FONT = next((n for n in ['Malgun Gothic', 'AppleGothic', 'NanumGothic',
                         'Noto Sans CJK KR', 'Noto Sans CJK JP'] if n in installed), None)
# sns.set_theme()은 글꼴 설정을 초기화하므로 font= 로 한글 폰트를 함께 지정한다
sns.set_theme(style='whitegrid', font=FONT, rc={'axes.unicode_minus': False})
pd.set_option('display.width', 200)  # 출력 폭을 넓혀 컬럼이 줄바꿈되지 않게 한다


# ============================================================
# [1] 데이터 읽기
# ============================================================
df = pd.read_csv(DATA_DIR / 'bread_basket.csv')
print('크기 :', df.shape)  # (20507, 5)
print(df.head())
print('영수증 수 :', df['Transaction'].nunique())  # 9465
print('상품 종류 :', df['Item'].nunique())  # 94
print('기간 :', df['date_time'].min(), '~', df['date_time'].max())  # 01-01-2017 01:21 ~ 31-12-2016 17:36
# ↑ 문자열끼리 비교해서 날짜 순서가 아니다. 아래 [2]에서 날짜로 바꾼 뒤 다시 확인한다.


# ============================================================
# [2] 전처리 : 상품이 아닌 행 제거, 날짜 변환, 본인 조건 추출
# ============================================================
print(df[df['Item'] == 'Adjustment'])  # 'Adjustment'는 계산 조정 기록이라 상품이 아님(1행)
df = df[df['Item'] != 'Adjustment'].copy()

# date_time은 '일-월-연도 시:분' 형식의 문자열이다. format을 지정해야 월과 일이 뒤바뀌지 않는다.
df['date_time'] = pd.to_datetime(df['date_time'], format='%d-%m-%Y %H:%M')
print('기간 :', df['date_time'].min(), '~', df['date_time'].max())  # 2016-10-30 09:58 ~ 2017-04-09 15:04
df['월'] = df['date_time'].dt.strftime('%Y-%m')  # '2017-02' 형태의 문자열

my = df[(df['월'] == MONTH) & (df['weekday_weekend'] == DAY_TYPE)].copy()  # 본인 조건의 판매 기록
print(f'본인 조건 {MONTH} {DAY_TYPE} : {len(my)}행, 영수증 {my["Transaction"].nunique()}건')
# 본인 조건 2017-02 weekend : 1529행, 영수증 603건


# ============================================================
# [3] 많이 팔린 상품 상위 10개 (가로 막대그래프)
# ============================================================
# 한 영수증에 같은 상품이 여러 줄 있을 수 있으므로 '그 상품이 들어간 영수증 수'로 센다
item_cnt = my.groupby('Item')['Transaction'].nunique().sort_values(ascending=False)
top10 = item_cnt.head(10)
print(top10)

plt.figure(figsize=(8, 5))
ax = sns.barplot(x=top10.values, y=top10.index, color='#4472C4')  # 가로 막대(한 가지 색)
for i, v in enumerate(top10.values):  # 막대 끝에 값 표시
    ax.text(v, i, f' {v}', va='center', fontsize=9)
ax.set_title(f'많이 팔린 상품 상위 10개 ({MONTH} {DAY_TYPE})')
ax.set_xlabel('상품이 들어간 영수증 수')
ax.set_ylabel('')
plt.tight_layout()
plt.savefig(OUT_DIR / '실습2_3_상위10상품.png', dpi=120)
plt.show()


# ============================================================
# [4] 장바구니 표 만들기 (행 : 영수증, 열 : 상품, 값 : True/False)
# ============================================================
trans = my[['Transaction', 'Item']].drop_duplicates()  # 같은 영수증의 중복 상품은 하나로
trans = trans.groupby('Transaction')['Item'].apply(list)  # 영수증별 상품 목록
print(trans.head())

te = TransactionEncoder()
basket = pd.DataFrame(te.fit(trans).transform(trans), columns=te.columns_)
print('장바구니 표 크기 :', basket.shape)  # (영수증 수, 상품 종류 수) → (603, 45)


# ============================================================
# [5] 빈발 항목집합 (지지도 2% 이상)
# ============================================================
freq_item = apriori(df=basket, min_support=MIN_SUPPORT, use_colnames=True)
print('빈발 항목집합 수 :', len(freq_item))  # 41
print(freq_item.sort_values('support', ascending=False).head(10))


# ============================================================
# [6] 연관규칙 : 향상도 1 이상, 신뢰도 상위 10개
# ============================================================
rules = association_rules(df=freq_item, metric='lift', min_threshold=1,  # 향상도 1 이상
                          num_itemsets=len(basket))  # 전체 영수증 수
print('규칙 수 :', len(rules))  # 28

# frozenset({'Coffee'}) 형태는 읽기 어려우므로 'Coffee' 같은 문자열로 바꾼 컬럼을 만든다
rules['앞'] = rules['antecedents'].apply(lambda s: ', '.join(sorted(s)))
rules['뒤'] = rules['consequents'].apply(lambda s: ', '.join(sorted(s)))
cols = ['앞', '뒤', 'support', 'confidence', 'lift']

rules = rules.sort_values('confidence', ascending=False)  # 신뢰도 높은 순
print(rules[cols].head(10).round(3).to_string(index=False))


# ============================================================
# [7] 규칙 산점도 : x 지지도, y 신뢰도, 색 향상도
# ============================================================
plt.figure(figsize=(8, 6))
ax = sns.scatterplot(data=rules, x='support', y='confidence',
                     hue='lift', palette='Blues',  # 향상도가 클수록 진한 파랑
                     size='lift', sizes=(40, 300),  # 향상도가 클수록 큰 점
                     edgecolor='gray')
for _, r in rules.sort_values('lift', ascending=False).head(5).iterrows():  # 향상도 상위 5개만 이름 표시
    ax.annotate(f"{r['앞']} → {r['뒤']}", (r['support'], r['confidence']),
                xytext=(10, 0), textcoords='offset points',  # 점에서 오른쪽으로 10pt 띄워 표시
                va='center', fontsize=8)
ax.set_title(f'연관규칙 {len(rules)}개의 지지도·신뢰도·향상도 ({MONTH} {DAY_TYPE})')
ax.set_xlabel('지지도 (support)')
ax.set_ylabel('신뢰도 (confidence)')
ax.legend(title='향상도', loc='upper right')
plt.tight_layout()
plt.savefig(OUT_DIR / '실습2_7_규칙산점도.png', dpi=120)
plt.show()


# ============================================================
# [8] 결과에 Coffee가 없는 규칙 중 향상도 상위 5개
# ============================================================
# Coffee는 영수증의 절반 가까이에 들어가는 인기 상품이라 '→ Coffee' 규칙은 신뢰도가 높게 나오기 쉽다.
# 이를 빼고 향상도로 정렬하면 인기 상품에 묻혀 있던 조합이 보인다.
no_coffee = rules[~rules['consequents'].apply(lambda s: 'Coffee' in s)]
print(no_coffee.sort_values('lift', ascending=False)[cols].head(5).round(3).to_string(index=False))


# ============================================================
# [9] 오전·오후 비교 : {Coffee} → ? 규칙 중 신뢰도 1위
# ============================================================
for period in ['morning', 'afternoon']:
    part = my[my['period_day'] == period]  # 해당 시간대의 판매 기록
    t = part[['Transaction', 'Item']].drop_duplicates().groupby('Transaction')['Item'].apply(list)
    te_p = TransactionEncoder()
    b = pd.DataFrame(te_p.fit(t).transform(t), columns=te_p.columns_)
    f = apriori(df=b, min_support=MIN_SUPPORT, use_colnames=True)
    r = association_rules(df=f, metric='lift', min_threshold=1, num_itemsets=len(b))
    r = r[r['antecedents'] == frozenset({'Coffee'})]  # 앞이 Coffee 하나인 규칙만
    r = r.sort_values('confidence', ascending=False)
    print(f'[{period}] 영수증 {len(b)}건, Coffee → ? 규칙 {len(r)}개')
    if len(r) > 0:
        best = r.iloc[0]
        print(f"  1위 : Coffee → {', '.join(best['consequents'])} "
              f"(신뢰도 {best['confidence']:.3f}, 향상도 {best['lift']:.3f})")


# ============================================================
# [10] 해석 : 6번과 8번의 결과 비교 및 빵집 세트/진열 전략 제안
# ============================================================
reason_diff = """
============================================================
[10] 과제 해석 및 비즈니스 제안
============================================================
1. [6]번과 [8]번의 결과가 다른 이유:
   - [6]번(신뢰도 기준 상위 10개)은 결과(consequents)가 대부분 'Coffee'로 나타납니다.
     이는 Coffee가 전체 영수증의 40% 이상에 포함되는 압도적인 베스트셀러이기 때문에,
     어떤 상품과 함께 구매되더라도 신뢰도(P(Coffee|X))가 구조적으로 높게 측정되는
     '인기 상품 편향(Popularity Bias)' 현상이 발생하기 때문입니다.
   - 반면 [8]번은 이러한 인기 편향을 제거하기 위해 Coffee를 제외하고 '향상도(Lift)'를
     기준으로 정렬했습니다. 향상도는 두 상품의 독립 발생 확률 대비 동시 발생 확률을
     평가하므로, 전체 판매량에 가려져 있던 순수한 상품 간의 강한 결합 관계를 보여줍니다.

2. 빵집에 제안할 세트 메뉴 및 진열 전략:
   [제안 1: 'Scone + Tea' 애프터눈 티 세트 및 인접 진열]
   - 근거 수치:
     * Scone → Tea (신뢰도: 0.261, 향상도: 2.022)
     * Tea → Scone (신뢰도: 0.176, 향상도: 2.022)
     스콘 구매 고객이 차(Tea)를 함께 구매할 확률은 일반 고객 대비 2.02배 높습니다.
   - 실행 방안:
     오후 시간대 티(Tea) 주문 시 스콘을 함께 묶은 '애프터눈 티 세트'를 구성하고,
     카운터 차 메뉴판 바로 옆에 스콘 진열대를 배치하여 동반 구매를 유도합니다.

   [제안 2: 'Pastry + Medialuna' 베이커리 듀오 번들]
   - 근거 수치:
     * Pastry → Medialuna (신뢰도: 0.308, 향상도: 2.845)
     * Medialuna → Pastry (신뢰도: 0.211, 향상도: 2.845)
     비커피 항목 중 가장 높은 향상도(2.845)와 높은 신뢰도(30.8%)를 기록했습니다.
   - 실행 방안:
     두 빵을 베이커리 매대에서 나란히 배치하거나 아침 출근·브런치용 묶음 세트로 포장 판매합니다.
============================================================
"""
print(reason_diff)
