import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

beers = [5, 2, 9, 8, 3, 7, 3, 5, 3, 5]  # 데이터 입력(음주량)
bal = [0.1, 0.03, 0.19, 0.12, 0.04, 0.0095, 0.07,  # 데이터 입력(혈중알코올농도)
       0.06, 0.02, 0.05]

dict = {'beers': beers, 'bal': bal}  # 딕셔너리 정의
df = pd.DataFrame(dict)  # 데이터프레임 생성
print(f'\n[df] 데이터프레임\n{df}')

df.plot.scatter(x='beers', y='bal',  # 산점도
                title='Beers~Blood Alcohol Level')
plt.show()

# 회귀선을 포함한 산점도
df.plot.scatter(x='beers', y='bal', title='Beers~Blood Alcohol Level')  # 산점도

m, b = np.polyfit(beers, bal, 1)  # 회귀식 계산
plt.plot(beers, m * np.array(beers) + b)  # 회귀선 출력
plt.show()

# 두 변수 간 상관계수 계산
print(f"\n[df['beers'].corr(df['bal'])] 상관계수 계산: "
      f"{df['beers'].corr(df['bal'])}")
