# 코드 4-5: 데이터프레임에 사칙연산을 적용하고 apply()로 조건부 계산을 하는 예제

# 코드 4-1 #########################################################
import pandas as pd

df = pd.read_csv("data/iris.csv")  # csv 파일 읽기

# 코드 4-1에 이어서 실행 ##############################################

# 데이터프레임 객체에 대한 산술 연산
# 산술 연산은 숫자형 컬럼에만 쓸 수 있으므로 문자열 컬럼인 'Species'를 먼저 빼낸다

# 'Species' 컬럼 제외
# df.columns != 'Species' 는 컬럼마다 True/False를 만들어 'Species'만 False가 된다
print(f"\n[df.loc[:, df.columns != 'Species']]\n{df.loc[:, df.columns != 'Species']}")

# 'Species' 컬럼 제외
# isin()은 목록에 포함되는지를 검사하고, ~는 결과를 뒤집는다. 제외할 컬럼이 여러 개일 때 편하다
print(f"\n[df.loc[:, ~df.columns.isin(['Species'])]]\n{df.loc[:, ~df.columns.isin(['Species'])]}")

# 모든 값에 10을 더함
# 하나의 숫자를 데이터프레임에 연산하면 모든 원소에 똑같이 적용된다 (브로드캐스팅)
print(f"\n[df.loc[:, df.columns != 'Species'] + 10]\n{df.loc[:, df.columns != 'Species'] + 10}")

# 두 컬럼의 같은 행 값들끼리 연산
# 반복문 없이 같은 인덱스끼리 자동으로 짝지어 계산된다 (벡터화 연산)
print(f"\n[df['Sepal_Length'] + df['Petal_Length']]\n{df['Sepal_Length'] + df['Petal_Length']}")

# apply()는 컬럼의 값을 하나씩 함수에 넣어 그 결과로 새 시리즈를 만든다
# lambda는 이름 없이 그 자리에서 만드는 간단한 함수이다
tmp = df['Petal_Length'].apply(lambda x: -1 if x >= 5 else 1)
print(f"\n[tmp]\n{tmp}")  # 5 이상이면 -1, 아니면 1이 들어 있다

# 원래 값에 tmp를 곱하면 5 이상인 값만 부호가 바뀐다
print(f"\n[df['Petal_Length'] * tmp]\n{df['Petal_Length'] * tmp}")
