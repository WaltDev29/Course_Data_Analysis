# flights 데이터로 월별·연도별 탑승객 수 선그래프를 그리는 예제
import seaborn as sns  # 통계 시각화 라이브러리
import matplotlib.pyplot as plt  # 그래프 출력용 라이브러리

df = sns.load_dataset('flights')  # seaborn 내장 데이터셋(연도·월별 항공기 탑승객 수) 불러오기
print(df.head())  # 앞 5행 확인

# 그래프 테마 설정
sns.set_theme(style="whitegrid", rc={"figure.figsize": (8, 5)})  # 흰 배경+격자, 그림 크기 8x5인치
sns.set_palette('hls', 12)  # 12개월을 구분하기 위해 12가지 색 사용

# 월별, 연도별 항공기 탑승객 수
sns.lineplot(data=df,  # df 이름
             x='year',  # x축 컬럼
             y='passengers',  # y축 컬럼
             hue='month'  # 그룹 지정
             )
plt.show()  # 그래프 화면에 출력
