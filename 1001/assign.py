import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

BASEDIR = Path(__file__).resolve().parents[1] / "data"

df_orig = pd.read_csv(BASEDIR / "airquality.csv")

# print(df_orig.info())

print("====== 열별 결측치 개수 ======")
print(df_orig.isna().sum())

print("\n====== 결측치 존재 행 개수 ======")
print(df_orig.loc[df_orig.isna().sum(axis=1) > 0].size)

print("\n====== 결측치 제거 DataFrame ======")
df_cleaned = df_orig.dropna(ignore_index=True)
print(df_cleaned)

print("\n====== IQR 기반 이상치 제거 ======")

sw = df_cleaned["Ozone"]

# IQR 이용

Q1 = sw.quantile(0.25)  # 1사분위수(하위 25% 지점)
Q3 = sw.quantile(0.75)  # 3사분위수(하위 75% 지점)
IQR = Q3 - Q1  # 사분위 범위(가운데 50% 데이터의 폭)

# Q1 - 1.5×IQR보다 작거나 Q3 + 1.5×IQR보다 큰 값을 특잇값으로 판단
outliers = sw[(sw < Q1 - IQR*1.5) | (sw > Q3 + IQR*1.5)]
print('[IQR 기준 특잇값]', outliers, sep='\n')

# 특잇값 제거
df_cleaned = df_cleaned.loc[~df_cleaned["Ozone"].isin(outliers)]  # isin: 특잇값에 포함되는지 확인, ~: True/False 반전
print('\n[특잇값 제거 후 데이터 개수]', len(df_cleaned), sep='\n')

print("\n", df_cleaned)

# ====== 월별 데이터 평균 그래프 시각화 ======
monthly = df_cleaned.groupby("Month")[["Ozone", "Solar.R", "Wind", "Temp"]].mean()
monthly.plot(kind="line", marker="o")
plt.show()