# 코드 3-8 #########################################################
# 값의 수정, 추가, 삭제
import pandas as pd

salary = pd.Series([20, 15, 18, 30])  # 레이블 인덱스가 없는 시리즈 객체
score = pd.Series([75, 80, 90, 60],
                  index=['KOR', 'ENG', 'MATH', 'SOC'])

# 값의 변경
score.iloc[0] = 85  # 인덱스 0의 값을 변경
score.loc['SOC'] = 65  # 인덱스 'SOC'의 값을 변경
score.loc[['ENG', 'MATH']] = [70, 80]  # 인덱스 'ENG','MATH'의 값을 변경

# 코드3-8에 이어서 실행  ####################################################

# 값의 추가 (레이블 인덱스가 있는 경우)
score.loc['PHY'] = 50  # 없는 인덱스 추가
print(score)
score.iloc[5] = 90  # 에러 발생

# 값의 추가 (레이블 인덱스가 없는 경우)
next_idx = salary.size
salary.iloc[next_idx] = 33  # 에러 발생
salary.loc[next_idx] = 33  # 정상 수행
print(salary)

# _append() 메서드를 이용한 값의 추가
new = pd.Series({'MUS': 95})
print(score._append(new))  # score에 변경 없음
print(score)
score = score._append(new)  # score가 변경됨
print(score)

print(salary._append(pd.Series([66]), ignore_index=True))
salary = salary._append(pd.Series([66]), ignore_index=True)
print(salary)
