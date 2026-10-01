# 임의 샘플링, 층화 샘플링, 조합 만들기
import pandas as pd
import itertools  # 조합·순열을 만드는 표준 라이브러리
from pathlib import Path

# 이 파일의 위치를 기준으로 데이터 폴더를 찾는다(어느 폴더에서 실행해도 동작)
DATA_DIR = Path(__file__).resolve().parents[2] / 'data'

df = pd.read_csv(DATA_DIR / 'iris.csv')

# 임의 샘플링: 전체 150행 중 20행을 무작위로 추출
# random_state: 난수 고정값(같은 값이면 실행할 때마다 같은 행이 뽑힘)
df20 = df.sample(n=20, random_state=123)
print('[임의 샘플링(20개)]', df20, sep='\n')

# 층화 샘플링: 품종(Species)별로 그룹을 나눈 뒤 각 그룹에서 같은 비율로 추출
# frac=0.2: 그룹마다 20%씩 추출(품종별 50행 -> 10행씩, 총 30행)
stratified = df.groupby('Species').apply(
    lambda x: x.sample(frac=0.2, random_state=123)  # x: 품종 하나의 데이터
)
print('[층화 샘플링(품종별 20%)]', stratified, sep='\n')

# 조합: 품종 3개 중 2개를 뽑는 모든 경우(순서 무관, 3C2 = 3가지)
species = df.Species.unique()  # 중복을 제거한 품종 목록

comb = list(itertools.combinations(species, 2))  # 결과를 리스트로 변환
print('[품종 2개 조합]', comb, sep='\n')
