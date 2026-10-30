# 치폴레 주문 데이터로 함께 팔리는 메뉴를 찾는 연관 분석(장바구니 분석) 예제
import pandas as pd  # 데이터 처리 라이브러리
import matplotlib.pyplot as plt  # 그래프 출력용 라이브러리
from mlxtend.frequent_patterns import association_rules, apriori  # 연관규칙 생성, 빈발 항목집합 탐색
from mlxtend.preprocessing import TransactionEncoder  # 주문별 메뉴 목록을 0/1 표로 변환
from pathlib import Path  # 파일 경로 처리용

# 이 파일의 위치를 기준으로 데이터 폴더를 찾는다(어느 폴더에서 실행해도 동작)
DATA_DIR = Path(__file__).resolve().parents[1] / 'data'

# (1) 데이터 준비
df = pd.read_csv(DATA_DIR / 'chipotle.csv')  # 치폴레 주문 데이터 읽기(Transaction: 주문 번호, Item: 메뉴)

df.info()  # 컬럼 자료형과 결측값 확인
print(df.iloc[:, [0, 1, 2, 4]].head())  # 일부 컬럼의 앞 5행 확인

# (2) 데이터 탐색
print(len(df['Item'].unique()))  # 음식의 종류
temp = df[df.item_price == df.item_price.max()]  # 가장 비싼 음식
temp = temp[['Item', 'item_price']].drop_duplicates()  # 메뉴명·가격만 남기고 중복 제거
print(temp)  # 결과 확인

temp = df[df.item_price == df.item_price.min()]  # 가장 저렴한 음식
temp = temp[['Item', 'item_price']].drop_duplicates()  # 메뉴명·가격만 남기고 중복 제거
print(temp)  # 결과 확인

print(len(df['Transaction'].unique()))  # 트랜잭션 수

# 많이 판매된 음식
sales_quantity = df.groupby('Item').count()  # 메뉴별 행 개수(그 메뉴가 등장한 주문 줄 수, quantity 합계가 아님)
sales_quantity = sales_quantity.sort_values('Transaction', ascending=False)  # 등장 횟수가 많은 순 정렬
print(sales_quantity['Transaction'])  # 메뉴별 등장 횟수 확인(Transaction 컬럼의 값 개수일 뿐, 주문 번호가 아님)

# 매출 상위 10개 상품
top_ten = sales_quantity.sort_values('Transaction').tail(10)  # 오름차순 정렬 후 마지막 10개(그래프 위쪽이 큰 값)
top_ten = top_ten['Transaction']  # 등장 횟수만 사용

top_ten.plot.barh(xlabel='Transaction',  # x축 레이블
                  ylabel='',  # y축 레이블
                  title='Top 10 Items',  # 그래프 제목
                  figsize=(9, 5))  # 그래프 크기(인치)
plt.subplots_adjust(left=0.2)  # 그래프 왼쪽 여백
plt.show()  # 그래프 화면에 출력

# (3) 연관 분석
# 전처리
temp = df[['Transaction', 'Item']].drop_duplicates()  # 한 주문에 같은 메뉴가 여러 번 있으면 하나로
temp = temp.groupby('Transaction')['Item'].apply(list)  # 주문별 메뉴 목록(장바구니) 만들기
print(temp)  # 결과 확인

te = TransactionEncoder()  # 장바구니 → 0/1 표 변환기
trans_matrix = te.fit(temp).transform(temp)  # 행: 주문, 열: 메뉴, 값: 포함 여부(True/False)
print(trans_matrix)  # 결과 확인

basket = pd.DataFrame(trans_matrix, columns=te.columns_)  # 열 이름을 메뉴명으로 붙여 데이터프레임으로
print(basket.head())  # 앞 5행 확인

# 연관규칙 탐색
freq_item = apriori(df=basket, min_support=0.01, use_colnames=True)  # 전체 주문의 1% 이상에 등장하는 메뉴 조합
print(freq_item)  # 빈발 항목집합 확인

rules = association_rules(df=freq_item, metric='lift', min_threshold=1,  # 향상도(lift) 1 이상인 규칙만
                          num_itemsets=len(basket))  # 전체 주문 수
rules.sort_values('confidence', ascending=False, inplace=True)  # 신뢰도가 높은 순 정렬
print(rules.head(10))  # 상위 10개 규칙 확인
print(rules.iloc[0, :].transpose())  # 가장 신뢰도가 높은 규칙의 지표를 세로로 확인