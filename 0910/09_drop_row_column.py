# 코드 4-9: drop()으로 데이터프레임의 행과 컬럼을 삭제하는 예제

# 코드 4-1 #########################################################
import pandas as pd

df = pd.read_csv("data/iris.csv")  # csv 파일 읽기

# 코드 4-1에 이어서 실행 ##################################################

# 데이터프레임 객체에 대한 행과 컬럼의 삭제
df5 = df.copy()  # 원본을 지키기 위해 복사본으로 작업한다

# 행의 삭제
# drop()은 원본을 바꾸지 않고 삭제된 새 데이터프레임을 돌려주므로 다시 대입해야 한다
df5 = df5.drop(index=[1, 3])
print(f'\n[df5] 1, 3행 삭제 후\n{df5}')  # 인덱스가 0, 2, 4...로 비어 있는 것을 확인한다

# reset_index()는 비어 있는 인덱스를 0부터 다시 붙인다
# 기존 인덱스는 'index'라는 컬럼으로 남는데, 필요 없다면 drop=True를 넣어 없앤다
df5 = df5.reset_index()
print(f'\n[df5] reset_index() 후\n{df5}')

# 컬럼의 삭제
# index= 대신 columns=를 쓰면 컬럼이 삭제된다
df5 = df5.drop(columns='Petal_Length')
print(f"\n[df5] 'Petal_Length' 컬럼 삭제 후\n{df5}")
