# concat으로 데이터프레임 이어 붙이기(행 방향, 열 방향)
import pandas as pd

df1 = pd.DataFrame([[169, 58, 1.0],
                    [172, 73, 1.2],
                    [184, 82, 0.7]],
                   columns=['height', 'weight', 'eye'])
df2 = pd.DataFrame([[176, 71, 0.8, 'M'],
                    [169, 62, 0.7, 'F'],
                    [158, 60, 1.3, 'M']],
                   columns=['height', 'weight', 'eye', 'gender'])  # df1에 없는 gender 컬럼이 있음
df3 = pd.DataFrame([[3, 22],
                    [2, 21]],
                   columns=['grade', 'age'])  # 행이 2개뿐

print('[df1]', df1, sep='\n')
print('[df2]', df2, sep='\n')
print('[df3]', df3, sep='\n')

df12 = pd.concat([df1, df2])  # 행 방향 병합(df1에는 gender가 없어 NaN으로 채워짐)
print('[행 방향 병합(df1 + df2)]', df12, sep='\n')
df12 = df12.reset_index(drop=True)  # 인덱스가 0,1,2,0,1,2로 겹치므로 0~5로 다시 매김
print('[인덱스 초기화 후 행 방향 병합]', df12, sep='\n')
df13 = pd.concat([df1, df3], axis=1)  # 열 방향 병합(인덱스 기준, df3에 없는 2행은 NaN)
print('[열 방향 병합(df1 + df3)]', df13, sep='\n')
