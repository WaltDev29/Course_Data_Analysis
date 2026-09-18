import pandas as pd
import matplotlib.pyplot as plt

# 시계열 데이터에 대한 복수의 선그래프 그리기
late1 = [5, 8, 7, 9, 4, 6, 12, 13, 8, 6, 6, 4]
late2 = [4, 6, 5, 8, 7, 8, 10, 11, 6, 5, 7, 3]

dict = {'class_1': late1, 'class_2': late2}

late = pd.DataFrame(dict,
                    index=list(range(1, 13)))

print(f'\n[late] 월별 지각생 수\n{late}')

late.plot(title='Late student per month',  # 제목
          xlabel='month',  # x축 레이블
          ylabel='frequency',  # y축 레이블
          marker='o')  # 점의 종류

plt.legend(loc='upper right')  # 범례 지정
plt.show()
