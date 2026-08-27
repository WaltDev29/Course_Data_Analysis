import pandas as pd

age = pd.Series([25, 34, 19, 45, 60])
age.index = ['John', 'Jane', 'Tom', 'Micle', 'Tom']
print(age, "\n")

print(age.iloc[3])
print(age.loc['Tom'])
