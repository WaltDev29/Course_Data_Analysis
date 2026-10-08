# tips 데이터로 막대그래프(그룹별·누적)를 그리는 예제
import seaborn as sns  # 통계 시각화 라이브러리
import matplotlib.pyplot as plt  # 그래프 출력용 라이브러리
df = sns.load_dataset('tips')  # seaborn 내장 데이터셋(식당 팁 데이터) 불러오기
print(df.head())  # 앞 5행 확인

# 그래프 테마 설정
sns.set_theme(style="whitegrid", rc={"figure.figsize": (5, 5)})  # 흰 배경+격자, 그림 크기 5x5인치
sns.set_palette('hls', 4)  # hls 팔레트에서 4가지 색 사용

# 요일별 평균 지불 금액
sns.barplot(data=df,  # df 이름
            x='day',  # x축 컬럼
            y='total_bill',  # y축 컬럼
            estimator='mean',  # y축 컬럼 적용 함수
            hue='day',  # 그룹 지정
            legend=None  # 범례 표시 안 함
            )
plt.show()  # 그래프 화면에 출력

# 요일별 성별 평균 지불 금액
sns.barplot(data=df,  # df 이름
            x='day',  # x축 컬럼
            y='total_bill',  # y축 컬럼
            estimator='mean',  # y축 컬럼 적용 함수
            hue='sex',  # y축 값의 그룹핑 기준
            errorbar=None  # 에러선 삭제
            )
plt.show()  # 그래프 화면에 출력

# 누적 막대그래프
df2 = df.pivot_table(index='day',  # 행 위치에 들어갈 컬럼
                     columns='sex',  # 열 위치에 들어갈 컬럼
                     values='total_bill',  # 데이터로 사용할 컬럼
                     aggfunc='mean'  # 데이터 집계함수
                     )
print(df2)  # 피벗 테이블 결과 확인
df2.plot.bar(stacked=True)  # pandas 내장 기능으로 누적 막대그래프 작성
plt.subplots_adjust(bottom=0.2)  # x축 레이블이 잘리지 않도록 하단 여백 확보
plt.show()  # 그래프 화면에 출력
