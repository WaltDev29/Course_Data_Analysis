import pandas as pd
import numpy as np

# 데이터 입력
temp = pd.Series([-0.8, -0.1, 7.7, 13.8, 18.0, 22.4,
                  25.9, 25.3, 21.0, 14.0, 9.6, -1.4])
print(temp)  # temp의 내용 확인

# 월 이름을 레이블 인덱스로 지정하기
print(temp.index)  # 인덱스 내용 확인
temp.index = ['1월', '2월', '3월', '4월',  # 월 이름을 인덱스로 지정
              '5월', '6월', '7월', '8월',
              '9월', '10월', '11월', '12월']
print(temp)  # temp의 내용 확인
