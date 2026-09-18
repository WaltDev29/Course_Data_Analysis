# 값의 수정, 추가, 삭제
import pandas as pd

salary = pd.Series([20, 15, 18, 30])  # 레이블 인덱스가 없는 시리즈 객체
score = pd.Series([75, 80, 90, 60],
                  index=['KOR', 'ENG', 'MATH', 'SOC'])
print(salary)
print(score)

# 값의 변경
score.iloc[0] = 85  # 인덱스 0의 값을 변경
print(score)
score.loc['SOC'] = 65  # 인덱스 'SOC'의 값을 변경
print(score)
score.loc[['ENG', 'MATH']] = [70, 80]  # 인덱스 'ENG', 'MATH'의 값을 변경
print(score)
