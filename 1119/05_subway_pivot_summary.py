# subway 테이블에서 출근 시간대 승객 수를 조회해 호선별·승객유형별 피벗 테이블로 요약하는 예제

import os
from pathlib import Path
# 이 파일이 있는 폴더(Ch13)로 이동 → 같은 폴더의 SQLite.py 를 불러올 수 있음
os.chdir(Path(__file__).resolve().parent)
from SQLite import *

SL = SQLite()  # SQLite 객체 생성

# 7~8시, 8~9시 두 시간대 인원을 더해 출근 시간대 승객 수를 구함
sql = "select 호선명, 승객유형, t07_08시간대+t08_09시간대 from subway"
result = SL.run_sql(sql)
print(result.head())   # 앞 5행 확인 (계산 컬럼 이름은 식 그대로 표시됨)

# 피벗 테이블 생성 (행: 호선명, 열: 승객유형, 값: 출근 시간대 승객 수 합계)
df_pivot = result.pivot_table(index='호선명',
                              columns='승객유형',
                              values='t07_08시간대+t08_09시간대',
                              aggfunc='sum')
print(df_pivot)

# csv 저장 (엑셀에서 한글이 깨지지 않도록 EUC-KR 인코딩 사용)
df_pivot.to_csv('subway_summary.csv', encoding='EUC-KR')

SL.close_db()  # DB 작업 종료
