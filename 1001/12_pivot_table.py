# 피벗 테이블로 두 범주 기준 집계표 만들기
import seaborn as sns

# 피벗 테이블 작성
df = sns.load_dataset('tips')  # 식당 계산 금액·팁 데이터(인터넷에서 내려받으므로 연결 필요)
print('[tips 데이터 앞부분]', df.head(), sep='\n')

# 성별(행) × 요일(열)별 계산 금액 평균
p1 = df.pivot_table(index='sex',  # 행 위치에 들어갈 컬럼
                    columns='day',  # 열 위치에 들어갈 컬럼
                    values='total_bill',  # 데이터로 사용할 컬럼
                    aggfunc='mean'  # 데이터 집계함수
                    )
print('[성별×요일 total_bill 평균]', p1.head(), sep='\n')

# 성별(행) × 시간대(열, 점심/저녁)별 계산 금액 평균
p2 = df.pivot_table(index='sex',  # 행 위치에 들어갈 컬럼
                    columns='time',  # 열 위치에 들어갈 컬럼
                    values='total_bill',  # 데이터로 사용할 컬럼
                    aggfunc='mean'  # 데이터 집계함수
                    )
print('[성별×시간대 total_bill 평균]', p2.head(), sep='\n')

# 시간대(행) × 요일(열)별 팁 최댓값(데이터가 없는 조합은 NaN)
p3 = df.pivot_table(index='time',  # 행 위치에 들어갈 컬럼
                    columns='day',  # 열 위치에 들어갈 컬럼
                    values='tip',  # 데이터로 사용할 컬럼
                    aggfunc='max'  # 데이터 집계함수
                    )
print('[시간대×요일 tip 최댓값]', p3.head(), sep='\n')
