# 코드 4-1: csv 파일을 읽어 판다스 데이터프레임으로 만들고 내용을 확인하는 예제

import pandas as pd  # 판다스를 pd라는 별칭으로 불러오기

# read_csv()는 csv 파일을 읽어 DataFrame(2차원 표 형태의 자료구조) 객체로 반환한다
# 경로는 이 스크립트가 실행되는 작업 폴더 기준의 상대경로이다
df = pd.read_csv('data/iris.csv')  # csv 파일 읽기

# 주피터 노트북에서는 df만 써도 표가 출력되지만,
# .py 파일로 실행할 때는 print()로 감싸야 화면에 보인다
print(df)  # 내용 확인
