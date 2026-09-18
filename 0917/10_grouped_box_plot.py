import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 이 파일의 위치를 기준으로 데이터 폴더를 찾는다(어느 폴더에서 실행해도 동작)
DATA_DIR = Path(__file__).resolve().parents[1] / 'data'

# 데이터 불러오기
df = pd.read_csv(DATA_DIR / 'iris.csv')

# 상자그림 그리기
df.boxplot(column='Petal_Length',  # 상자그림 대상 컬럼
           by='Species',  # 그룹 정보 컬럼
           grid=False)  # 격자 표시 제거
plt.suptitle('')  # 기본 표시 제목 제거
plt.show()
