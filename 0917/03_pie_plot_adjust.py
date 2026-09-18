# 코드 5-1 #########################################################
import matplotlib.pyplot as plt
import pandas as pd

favorite = pd.Series(['WINTER', 'SUMMER', 'SPRING', 'SUMMER', 'SUMMER',
                      'FALL', 'FALL', 'SUMMER', 'SPRING', 'SPRING'])


fd = favorite.value_counts()  # 도수분포를 fd에 저장


# 원그래프 작성
fd.plot.pie(ylabel='',  # y축 레이블
            autopct='%1.0f%%',  # 백분율 출력 지정
            title='Favorite Season')  # 그래프 제목
plt.show()
