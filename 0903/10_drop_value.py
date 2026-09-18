# 값의 수정, 추가, 삭제
# 코드 3-8 #########################################################
import pandas as pd


# 코드3-8에 이어서 실행 ##################################################

# 값의 삭제
score = pd.Series([85, 70, 80, 65, 50, 95],
                  index=['KOR', 'ENG', 'MATH', 'SOC', 'PHY', 'MUS'])
salary = pd.Series([20,15,18,30,33])

print(score.drop('PHY'))  # 레이블 인덱스가 있는 경우
print(score)
score = score.drop('PHY')
print(score)

salary = salary.drop(1)  # 레이블 인덱스가 숫자인 경우
print(salary)
