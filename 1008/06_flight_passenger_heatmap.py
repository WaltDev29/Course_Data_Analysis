# flights 데이터로 월·연도별 탑승객 수 히트맵을 그리는 예제
import seaborn as sns  # 통계 시각화 라이브러리
import matplotlib.pyplot as plt  # 그래프 출력용 라이브러리

flights = sns.load_dataset('flights')  # seaborn 내장 데이터셋(연도·월별 항공기 탑승객 수) 불러오기
print(flights.head())  # 앞 5행 확인

# 피벗 테이블 생성
df = flights.pivot_table(index='month',  # 행 위치에 들어갈 컬럼
                         columns='year',  # 열 위치에 들어갈 컬럼
                         values='passengers',  # 데이터로 사용할 컬럼
                         aggfunc='mean'  # 데이터 집계함수
                         )
print(df.head())  # 피벗 결과 확인(행: 월, 열: 연도)

# 히트맵 작성
sns.set_theme(rc={'figure.figsize': (8, 7)})  # 그림 크기 8x7인치
sns.heatmap(df).set_title('Heatmap of Flight Passenger', fontsize=20)  # 값이 클수록 밝은 색으로 표시, 제목 지정
plt.show()  # 그래프 화면에 출력
