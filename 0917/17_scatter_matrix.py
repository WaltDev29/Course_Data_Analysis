import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 이 파일의 위치를 기준으로 데이터 폴더를 찾는다(어느 폴더에서 실행해도 동작)
DATA_DIR = Path(__file__).resolve().parents[1] / 'data'

# 데이터 읽기
df = pd.read_csv(DATA_DIR / 'mtcars.csv')

# 다중 산점도의 작성
vars = ['mpg', 'disp', 'drat', 'wt']
pd.plotting.scatter_matrix(df[vars])
plt.show()
