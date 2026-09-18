import pandas as pd
import numpy as np

# 산포 계산
mydata = pd.Series([60, 62, 64, 65, 68, 69, 72])

print(f'\n[mydata.var()] 분산: {mydata.var()}')
print(f'\n[mydata.std()] 표준편차: {mydata.std()}')
