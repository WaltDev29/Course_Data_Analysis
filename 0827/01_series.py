import pandas as pd

# 직접 리스트 입력
age = pd.Series([25, 34, 19, 45, 60])
print( age )                            # age의 내용 출력
print( type(age), "\n")                      # age의 데이터형 확인

# 이미 생성된 리스트 객체를 입력
data = ['spring', 'summer', 'fall', 'winter']
season = pd.Series(data)
print(season, "\n")

print(season.iloc[2])                 # 인덱스 2의 값
