# 코드 4-8: 데이터프레임에 행과 컬럼을 뒤쪽 또는 중간에 추가하는 예제

# 코드 4-7 #########################################################
import pandas as pd

df = pd.read_csv("data/iris.csv")  # csv 파일 읽기

# 데이터프레임 객체에 있는 값의 수정
df3 = df.copy()  # df를 df3로 복사
df3.iloc[1, 2] = 5.5  # 1행 2열의 값 수정

df3.loc[1, 'Petal_Length'] = 1.1
df3.loc[df.Petal_Length > 6.5, 'Petal_Length'] *= 100

# 코드 4-7에 이어서 실행 #######################################################

# 데이터프레임 객체에 대한 행과 컬럼의 추가

# 뒷부분에 새로운 행 추가
# 인덱스는 0부터 시작하므로 전체 행 개수가 곧 '다음 행 번호'가 된다
new_idx = df3.shape[0]  # 추가할 행 번호 결정
# 없는 인덱스에 loc으로 값을 넣으면 그 자리에 행이 새로 만들어진다
# 리스트의 값 순서는 컬럼 순서와 정확히 일치해야 한다
df3.loc[new_idx] = [1.1, 4.5, 3.4, 2.2, 'setosa']
print(f'\n[df3.tail()] 뒷부분에 행 추가 후\n{df3.tail()}')

# 중간에 새로운 행 추가
# 끼워 넣을 한 행을 데이터프레임으로 만든다. 컬럼 이름을 df3와 똑같이 맞춰야 한다
new_row = pd.DataFrame([[1.1, 2.2, 3.3, 4.4, 'virginica']],
                       columns=df3.columns)
print(f'\n[new_row]\n{new_row}')
# concat()은 여러 데이터프레임을 위아래로 이어 붙인다
# 앞 10행 + 새 행 + 나머지 순서로 붙이면 중간에 끼워 넣은 효과가 된다
# ignore_index=True는 이어 붙인 뒤 인덱스를 0부터 다시 매긴다
df3 = pd.concat([df3.iloc[:10], new_row, df3.iloc[10:]], ignore_index=True)
print(f'\n[df3.iloc[8:13, :]] 입력 결과 확인\n{df3.iloc[8:13, :]}')

# 여러 행 추가
# 대괄호 안에 리스트를 여러 개 넣으면 여러 행짜리 데이터프레임이 된다
ext = pd.DataFrame([[1.2, 3.5, 4.3, 3.1, 'setosa'],
                    [2.1, 3.2, 2.3, 5.2, 'versicolor']],
                   columns=df3.columns)
print(f'\n[ext]\n{ext}')
# 교재의 df3._append(ext, ...)는 판다스 3.0부터 제거되어 AttributeError가 발생한다
# concat()으로 이어 붙이면 같은 결과이고, 이쪽이 현재 권장되는 방법이다
df3 = pd.concat([df3, ext], ignore_index=True)
print(f'\n[df3] 여러 행 추가 후\n{df3}')

# 뒤쪽에 컬럼 추가
new_col = df3.Petal_Length * 10  # 기존 컬럼을 계산해 새 컬럼 값을 만든다
# 없는 컬럼 이름에 값을 대입하면 맨 뒤에 컬럼이 새로 생긴다
df3['new_col'] = new_col
print(f'\n[df3] 뒤쪽에 컬럼 추가 후\n{df3}')

# 중간에 컬럼 추가
df4 = df.copy()
# insert()는 원하는 위치에 컬럼을 끼워 넣는다. loc은 컬럼 번호, column은 새 컬럼 이름이다
# 반환값 없이 df4를 직접 바꾸므로 다시 대입하지 않는다
df4.insert(loc=2, column='new_col2', value=new_col)  # 컬럼 인덱스 2 위치에 추가
print(f'\n[df4] 중간에 컬럼 추가 후\n{df4}')
