# 코드 3-1 #########################################################
import pandas as pd
import numpy as np

# 자료의 입력
temp = pd.Series([-0.8, -0.1, 7.7, 13.8, 18.0, 22.4,
                  25.9, 25.3, 21.0, 14.0, 9.6, -1.4])

# 월 이름을 레이블 인덱스로 지정하기
temp.index = ['1월', '2월', '3월', '4월',  # 월 이름을 인덱스로 지정
              '5월', '6월', '7월', '8월',
              '9월', '10월', '11월', '12월']
print(temp)  # temp의 내용 확인

# 코드 3-1에 이어서 실행 ##############################################

# 통계 관련 메서드
print(temp.sum())  # 값들의 합계
print(temp.mean())  # 값들의 평균
print(temp.median())  # 값들의 중앙값
print(temp.max())  # 값들의 최댓값
print(temp.min())  # 값들의 최솟값
print(temp.std())  # 값들의 표준편차
print(temp.var())  # 값들의 분산
print(temp.abs())  # 값들의 절댓값
print(temp.describe())  # 기초 통계 정보
