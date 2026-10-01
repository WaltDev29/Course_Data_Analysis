# merge로 공통 컬럼 기준 병합(inner, left, right, outer)
import pandas as pd

df1 = pd.DataFrame([['a', 90], ['b', 80], ['c', 40]],
                   columns=['name', 'kor'])  # 국어 점수(a, b, c)
df2 = pd.DataFrame([['a', 75], ['b', 60], ['d', 90]],
                   columns=['name', 'math'])  # 수학 점수(a, b, d)

print('[df1]', df1, sep='\n')
print('[df2]', df2, sep='\n')

# on='name': name 값이 같은 행끼리 연결
df12 = df1.merge(df2, on='name')  # inner: 양쪽에 모두 있는 a, b만 남음(기본값)
print('[inner 병합]', df12, sep='\n')

df12 = df1.merge(df2, how='left', on='name')  # left: df1(a, b, c) 기준, c의 math는 NaN
print('[left 병합]', df12, sep='\n')

df12 = df1.merge(df2, how='right', on='name')  # right: df2(a, b, d) 기준, d의 kor는 NaN
print('[right 병합]', df12, sep='\n')

df12 = df1.merge(df2, how='outer', on='name')  # outer: 양쪽의 모든 이름(a, b, c, d), 없는 값은 NaN
print('[outer 병합]', df12, sep='\n')
