# 사용자 정의 클래스를 이용한 SQL 연습의 예

import os
from pathlib import Path
# 이 파일이 있는 폴더(Ch13)로 이동 → 같은 폴더의 SQLite.py 를 불러올 수 있음
os.chdir(Path(__file__).resolve().parent)
from SQLite import *              # SQLite.py 의 SQLite 클래스 불러오기
SL = SQLite()  # SQLite 객체 생성 (생성과 동시에 emp.db 연결)

sql = "select * from dept"
print(SL.run_sql(sql))  # 질의 결과 확인 (결과는 DataFrame)

# 문자열 끝의 \ 는 다음 줄로 이어 쓴다는 뜻
sql = "select * from emp \
    where sal > 2500"             # 급여가 2500 초과인 사원 조회
result = SL.run_sql(sql)
print(result)
print(result['SAL'].sum())  # 질의 결과 가공 (급여 합계)

SL.close_db()  # DB 작업 종료
