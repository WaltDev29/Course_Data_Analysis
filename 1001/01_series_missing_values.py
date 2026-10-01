# 결측값(NA)이 있는 Series의 계산과 확인·제거
import pandas as pd

# pd.NA: 판다스에서 결측값(값이 없음)을 나타내는 표기
score = pd.Series([30, 20, 40, pd.NA, 30, pd.NA])
print('[원본 score]', score, sep='\n')
print('[합계(결측값 제외)]', score.sum(), sep='\n')  # 결측값을 제외하고 계산
print('[평균(결측값 제외)]', score.mean(), sep='\n')  # 결측값을 제외하고 계산(값 4개의 평균)
print('[score + 5]', score + 5, sep='\n')  # 결측값은 산술 연산이 안 됨(결과도 결측값)

# isna(): 결측값이면 True, 아니면 False
print('[결측값 여부]', pd.isna(score), sep='\n')  # 결측값인지 확인
print('[결측값 개수]', pd.isna(score).sum(), sep='\n')  # 결측값의 개수 확인(True를 1로 계산)

print('[값의 개수(결측값 포함)]', score.size, sep='\n')  # 값의 개수(결측값 포함)
print('[값의 개수(결측값 제외)]', score.count(), sep='\n')  # 값의 개수(결측값 제외)

# notna(): isna()의 반대(결측값이 아니면 True)
print('[결측값이 아닌지 여부]', pd.notna(score), sep='\n')  # 결측값이 아닌지 확인
print('[결측값이 아닌 값의 개수]', pd.notna(score).sum(), sep='\n')  # 결측값이 아닌 값의 개수 확인

score = score.dropna()  # 결측값 제외(인덱스 3, 5가 빠져 번호가 중간중간 비게 됨)
print('[결측값 제거 후 score]', score, sep='\n')
score = score.reset_index(drop=True)  # 인덱스 초기화(0부터 다시 번호를 매기고 기존 인덱스는 버림)
print('[인덱스 초기화 후 score]', score, sep='\n')
