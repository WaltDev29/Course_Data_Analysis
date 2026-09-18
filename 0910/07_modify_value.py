# 코드 4-7: 데이터프레임의 특정 위치나 조건에 맞는 값을 수정하는 예제

# 코드 4-1 #########################################################
import pandas as pd

df = pd.read_csv("data/iris.csv")  # csv 파일 읽기

# 코드 4-1에 이어서 실행 ############################################

# 데이터프레임 객체에 있는 값의 수정
# copy()로 복사본을 만들어 작업한다. 복사하지 않고 df를 직접 고치면 원본이 훼손된다
df3 = df.copy()  # df를 df3로 복사

# iloc으로 위치를 지정해 값을 덮어쓴다 (1행, 2열 = Petal_Length)
df3.iloc[1, 2] = 5.5  # 1행 2열의 값 수정
print(f"\n[df3.iloc[1, 2] = 5.5 적용 후]\n{df3.head()}")

# loc으로 이름을 지정해 같은 자리를 다시 수정한다. 위와 같은 위치를 가리킨다
df3.loc[1, 'Petal_Length'] = 1.1
print(f"\n[df3.loc[1, 'Petal_Length'] = 1.1 적용 후]\n{df3.head()}")

# to_list()는 시리즈를 파이썬 리스트로 바꿔 준다. 값 전체를 한 줄로 훑어볼 때 편하다
# 시리즈를 리스트 형태로 출력
print(f"\n[df3.Petal_Length.to_list()] 수정 전\n{df3.Petal_Length.to_list()}")

# 조건에 맞는 여러 행의 값을 한 번에 수정한다
# 조건은 원본 df를 기준으로 잡고, 값은 복사본 df3에 반영된다
# *= 100 은 '기존 값에 100을 곱해서 다시 넣으라'는 뜻이다
df3.loc[df.Petal_Length > 6.5, 'Petal_Length'] *= 100
# 시리즈를 리스트 형태로 출력
print(f"\n[df3.Petal_Length.to_list()] 6.5 초과 값에 100을 곱한 후\n{df3.Petal_Length.to_list()}")
