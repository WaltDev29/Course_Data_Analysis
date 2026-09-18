import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 이 파일의 위치를 기준으로 데이터 폴더를 찾는다(어느 폴더에서 실행해도 동작)
DATA_DIR = Path(__file__).resolve().parents[1] / 'data'

# 데이터 읽기
df = pd.read_csv(DATA_DIR / 'mtcars.csv')

# 기본 산점도
df.plot.scatter(x='wt', y='mpg')
plt.show()

# 매개변수 조정 산점도
df.plot.scatter(x='wt',  # x축 변수명(중량)
                y='mpg',  # y축 변수명(연비)
                s=50,  # 점의 크기
                c='red',  # 점의 색
                marker='s')  # 점의 모양
plt.show()
