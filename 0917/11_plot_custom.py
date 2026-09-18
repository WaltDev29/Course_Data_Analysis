import pandas as pd
import matplotlib.pyplot as plt

favorite = pd.Series(['WINTER', 'SUMMER', 'SPRING', 'SUMMER', 'SUMMER',
                      'FALL', 'FALL', 'SUMMER', 'SPRING', 'SPRING'])

fd = favorite.value_counts()  # 도수분포를 fd에 저장

fd.plot.bar(xlabel='Season',  # x축 레이블
            ylabel='Frequency',  # y축 레이블
            rot=30,  # x축 값의 회전 각도
            title='Favorite Season',  # 그래프 제목
            color='b',  # 막대의 색
            grid=True,  # 격자 표시
            figsize=(6, 4)  # 그래프의 크기(inch)
            )

plt.subplots_adjust(bottom=0.2)  # 그래프 아래쪽 여백
plt.show()
