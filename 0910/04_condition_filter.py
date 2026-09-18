# 코드 4-4: 조건식(불리언 인덱싱)과 where()로 원하는 행만 골라내는 예제

# 코드 4-1 #########################################################
import pandas as pd

df = pd.read_csv("data/iris.csv")  # csv 파일 읽기

# 코드 4-1에 이어서 실행 ###########################################

# 조건문을 이용한 슬라이싱
# df.Petal_Length >= 6.5 는 각 행마다 True/False를 담은 시리즈를 만든다
# 이것을 loc에 넣으면 True인 행만 남는다 (불리언 인덱싱)

# 꽃잎의 길이가 6.5 이상인 행들의 모든 컬럼을 보이시오
print(f"\n[df.loc[df.Petal_Length >= 6.5, :]]\n{df.loc[df.Petal_Length >= 6.5, :]}")
# 모든 컬럼의 경우 컬럼 인덱스 생략
print(f"\n[df.loc[df.Petal_Length >= 6.5]]\n{df.loc[df.Petal_Length >= 6.5]}")

# 꽃잎의 길이가 6.5 이상인 행들의 인덱스 번호를 보이시오
# .index는 걸러진 결과가 원본의 몇 번째 행이었는지를 알려준다
print(f"\n[df.loc[df.Petal_Length >= 6.5].index]\n{df.loc[df.Petal_Length >= 6.5].index}")

# 꽃잎의 길이가 3.5~3.8 사이인 행들의 모든 컬럼을 보이시오
# 조건을 여러 개 묶을 때는 and/or가 아니라 &(그리고), |(또는)를 쓴다
# 우선순위 때문에 각 조건은 반드시 괄호로 감싸야 한다
print(f"\n[꽃잎 길이 3.5~3.8]\n"
      f"{df.loc[(df.Petal_Length >= 3.5) & (df.Petal_Length <= 3.8)]}")

# 꽃잎의 길이가 1.3 미만이거나 6.5를 초과하는 행들의 꽃잎의 길이와 폭을 보이시오
print(f"\n[꽃잎 길이 1.3 미만 또는 6.5 초과의 길이/폭]\n"
      f"{df.loc[(df.Petal_Length < 1.3) | (df.Petal_Length > 6.5), ['Petal_Length', 'Petal_Width']]}")

# where()를 이용한 조건 검색
# where()는 조건에 맞지 않는 행을 지우지 않고 NaN(결측치)으로 바꾼다
# 그래서 뒤에 dropna()를 붙여 NaN 행을 버려야 loc과 같은 결과가 된다
print(f"\n[df.where(df.Petal_Length >= 6.5).dropna()]\n"
      f"{df.where(df.Petal_Length >= 6.5).dropna()}")
