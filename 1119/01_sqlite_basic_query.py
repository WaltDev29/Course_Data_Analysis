# sqlite3 모듈로 DB에 연결해 테이블 목록과 dept 테이블을 조회하는 기본 예제

import sqlite3          # 파이썬 내장 SQLite 모듈
import pandas as pd
from pathlib import Path

# 이 파일의 위치를 기준으로 데이터 폴더를 찾는다(어느 폴더에서 실행해도 동작)
DATA_DIR = Path(__file__).resolve().parents[1] / 'data'

# DB 연결
conn = sqlite3.connect(DATA_DIR / 'emp.db')

# 커서 생성 (SQL 문을 실행하고 결과를 받아오는 역할)
cur = conn.cursor()

# 테이블 목록 조회 (sqlite_master: DB 안의 테이블·인덱스 정보를 담은 시스템 테이블)
cur.execute('SELECT name FROM sqlite_master WHERE type="table"')
result = cur.fetchall()   # [('dept',), ('emp',), ...] 형태의 튜플 리스트
print(result)

# dept 테이블의 전체 데이터 조회
cur.execute('SELECT * FROM dept')
result = cur.fetchall()
# cur.description 에서 컬럼 이름만 추출
columns = [column[0] for column in cur.description]
df_result = pd.DataFrame(result, columns=columns)   # 조회 결과를 DataFrame으로 변환
print(df_result)

cur.close()  # 커서 종료
conn.close()  # DB 연결 종료
