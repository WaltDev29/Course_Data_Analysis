import pandas as pd

# 2차원 리스트로부터 데이터프레임 생성
score = pd.DataFrame([[85, 96, 40, 95],
                      [73, 69, 45, 80],
                      [78, 50, 60, 90]])
print(score)  # score 내용 출력
print(type(score), "\n")  # score 자료형 출력

print(score.index)  # 행 방향 인덱스
print(score.columns, "\n")  # 열 방향 인덱스

print(score.iloc[1, 2])  # 인덱스 1행 2열의 값