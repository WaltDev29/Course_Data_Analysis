# 코드 5-1 #########################################################
import pandas as pd

favorite = pd.Series(['WINTER', 'SUMMER', 'SPRING', 'SUMMER', 'SUMMER',
                      'FALL', 'FALL', 'SUMMER', 'SPRING', 'SPRING'])


fd = favorite.value_counts()  # 도수분포를 fd에 저장
print(f'\n[favorite] favorite의 내용 출력\n{fd}')
# 코드 5-1에 이어서 실행 ################################################## 

import matplotlib.pyplot as plt
# 막대 그래프의 세로 출력
fd.plot.bar(xlabel='Season',  # x축 레이블
            ylabel='Frequency',  # y축 레이블
            rot=0,  # x축 값의 회전 각도
            title='Favorite Season')  # 그래프 제목
plt.show()

# 막대그래프의 가로 출력
fd.plot.barh(xlabel='Frequency',  # x축 레이블
             ylabel='Season',  # y축 레이블
             rot=0,  # x축 값의 회전 각도
             title='Favorite Season')  # 그래프 제목
plt.subplots_adjust(left=0.5)  # 그래프 왼쪽 여백 조정
plt.show()
