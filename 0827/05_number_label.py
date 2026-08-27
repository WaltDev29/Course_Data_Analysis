import pandas as pd

population = pd.Series([523, 675, 690, 720, 800])
population.index = [10, 20, 30, 40, 50]  # 숫자 레이블 지정
population
population.iloc[1]
population.iloc[20]  # 에러 발생
population.loc[20]
