# 코드 4-3: iloc/loc으로 데이터프레임의 특정 행과 컬럼을 인덱싱, 슬라이싱하는 예제

# 코드 4-1 #########################################################
import pandas as pd

df = pd.read_csv("data/iris.csv")  # csv 파일 읽기

# 코드 4-1에 이어서 실행 ##############################################

# 인덱싱과 슬라이싱
# iloc = 위치(정수 번호)로 접근, loc = 이름(라벨)으로 접근. 이 둘의 차이가 핵심이다

print(f"\n[df.iloc[2, 3]] 2행 3열의 값: {df.iloc[2, 3]}")  # 번호로 접근
print(f"\n[df.loc[3, 'Petal_Width']] 'Petal_Width' 컬럼의 3행 값: {df.loc[3, 'Petal_Width']}")  # 이름으로 접근

# 리스트를 넘기면 떨어져 있는 여러 행/컬럼을 한 번에 뽑을 수 있다
print(f"\n[df.loc[[0, 2, 4], ['Petal_Length', 'Petal_Width']]]\n"
      f"{df.loc[[0, 2, 4], ['Petal_Length', 'Petal_Width']]}")

# loc의 슬라이싱은 끝 값을 포함한다. 5:8은 5, 6, 7, 8행이다
print(f"\n[df.loc[5:8, 'Petal_Length']] 'Petal_Length' 컬럼의 5~8행 값\n"
      f"{df.loc[5:8, 'Petal_Length']}")

# iloc의 슬라이싱은 파이썬 리스트처럼 끝 값을 포함하지 않는다. :5는 0~4행이다
print(f"\n[df.iloc[:5, :4]] 0~4행, 0~3열의 값\n{df.iloc[:5, :4]}")

# 아래 세 가지는 모두 같은 결과(하나의 컬럼 = 시리즈)를 얻는 방법이다
print(f"\n[df.loc[:, 'Petal_Length']] 'Petal_Length' 컬럼의 모든 행의 값\n"
      f"{df.loc[:, 'Petal_Length']}")  # 콜론(:)은 '전체'를 의미한다
print(f"\n[df['Petal_Length']] 'Petal_Length' 컬럼의 모든 값\n{df['Petal_Length']}")  # 대괄호 방식
print(f"\n[df.Petal_Length] 'Petal_Length' 컬럼의 모든 값\n{df.Petal_Length}")  # 점(.) 방식, 컬럼명에 공백이 있으면 못 쓴다

# 컬럼 인덱스를 생략하면 모든 컬럼을 의미하므로 아래 두 줄의 결과는 같다
print(f"\n[df.iloc[:5, :]] 0~4행의 모든 컬럼의 값\n{df.iloc[:5, :]}")
print(f"\n[df.iloc[:5]] 0~4행의 모든 컬럼의 값\n{df.iloc[:5]}")
