import pandas as pd

# 1. 데이터 저장
data = [
    [-0.1, 1.8, 6.4, 12.3, 17.9, 22.2],
    [0.0, 2.0, 6.8, 12.9, 18.5, 22.8],
    [-0.1, 1.6, 5.8, 11.5, 17.1, 21.6],
    [-0.2, 1.6, 5.9, 11.5, 17.1, 21.5]]

data = pd.DataFrame(data).T
print("====== 1. ======\n", data, "\n")

columns = ["전북", "전주", "군산", "부안"]
data.columns = columns

index = ['1월', '2월', '3월', '4월', '5월', '6월']
data.index = index

print(data)

# 2. 전주 3월 평균 기온
print("2 : ", data.iloc[2,1])

# 3. 부안 4월 평균 기온
print("3 : ", data.iloc[3,3])

# 4. 군산 1월 평균 기온
print("4 : ", data.iloc[0,2])

# 5. 전북 6월 평균 기온
print("5 : ", data.iloc[5,0], "\n")

# 6. 전주 1~6월 평균 기온 시리즈
print("====== 6. ======\n", data.loc[:, "전주"], "\n")

# 7. 4개 지역 5월 평균 기온
print("====== 7. ======\n", data.loc["5월"], "\n")

# 8. 전주 - 군산
diff = round(data.loc['3월', '전주'] - data.loc['3월', '군산'], 1)
print("8 : ", diff)