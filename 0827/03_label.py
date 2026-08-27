import pandas as pd

# 시리즈에 레이블 부여
age = pd.Series([25, 34, 19, 45])
print(age, "\n")  # 레이블 부여 전
age.index = ['John', 'Jane', 'Tom', 'Luka']  # 행에 레이블 부여
print(age, "\n")  # 레이블 부여 후

print(age.iloc[2])  # 절대 위치에 의한 인덱싱
print(age.loc['Tom'])  # 레이블에 의한 인덱싱
# 데이터프레임에 레이블 부여

score = pd.DataFrame([[85, 96, 40, 95],
                      [73, 69, 45, 80],
                      [78, 50, 60, 90]])

print(score, "\n")  # 레이블 부여 전
score.index = ['John', 'Jane', 'Tom']  # 행에 레이블 부여
score.columns = ['KOR', 'ENG', 'MATH', 'SCI']  # 열에 레이블 부여
print(score, "\n")  # 레이블 부여 후

print(score.iloc[2, 1])  # 절대 위치에 의한 인덱싱
print(score.loc['Tom', 'ENG'])  # 레이블에 의한 인덱싱