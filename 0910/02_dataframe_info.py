# 코드 4-2: 데이터프레임의 구조(행/열 개수, 자료형, 컬럼명, 앞뒤 일부)를 확인하는 예제

# 코드 4-1 #########################################################
import pandas as pd

df = pd.read_csv("data/iris.csv")  # csv 파일 읽기

# 코드 4-1에 이어서 실행 #########################################

# 데이터프레임 객체의 정보 확인

# info()는 값을 반환하지 않고 스스로 화면에 출력하므로 print()로 감싸지 않는다
# 행 개수, 컬럼별 결측치가 아닌 값의 개수, 자료형, 메모리 사용량을 한 번에 보여준다
print('\n[df.info()] 배열의 정보')
df.info()  # 배열의 정보

# shape는 (행 개수, 컬럼 개수) 형태의 튜플이다. 메서드가 아니라 속성이므로 괄호가 없다
print(f'\n[df.shape] 배열의 형태: {df.shape}')
print(f'\n[df.shape[0]] 행의 개수: {df.shape[0]}')  # 튜플의 0번째 = 행 개수
print(f'\n[df.shape[1]] 컬럼의 개수: {df.shape[1]}')  # 튜플의 1번째 = 컬럼 개수

# dtypes는 컬럼별 자료형을 담은 시리즈이다. 숫자는 float64/int64, 문자열은 object로 나온다
print(f'\n[df.dtypes] 각 컬럼의 자료형\n{df.dtypes}')

# astype('category')는 값의 종류가 몇 개로 정해진 컬럼을 범주형으로 바꾼다
# 문자열(object)로 두는 것보다 메모리를 적게 쓰고, 그룹 연산이 빨라진다
df['Species'] = df['Species'].astype('category')
print(f'\n[df.dtypes] Species를 category로 변환한 뒤\n{df.dtypes}')

# columns는 컬럼 이름들을 담은 Index 객체이다
print(f'\n[df.columns] 컬럼들의 이름\n{df.columns}')

# 데이터가 많을 때 전체를 출력하는 대신 일부만 확인한다. 기본값은 5행이다
print(f'\n[df.head()] 데이터 앞부분 일부\n{df.head()}')
print(f'\n[df.tail()] 데이터 뒷부분 일부\n{df.tail()}')

# unique()는 컬럼에 들어 있는 값의 종류를 중복 없이 반환한다
print(f"\n[df['Species'].unique()] 품종 정보\n{df['Species'].unique()}")
