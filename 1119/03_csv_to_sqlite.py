# CSV 파일을 읽어 pandas의 to_sql()로 SQLite 테이블을 만드는 예제

import sqlite3
import pandas as pd
from pathlib import Path

# 이 파일의 위치를 기준으로 데이터 폴더를 찾는다(어느 폴더에서 실행해도 동작)
DATA_DIR = Path(__file__).resolve().parents[1] / 'data'

# DB 연결
conn = sqlite3.connect(DATA_DIR / 'emp.db')

# dept 테이블 생성
df = pd.read_csv(DATA_DIR / 'dept.csv')
# name: 테이블 이름, if_exists='replace': 같은 이름이 있으면 덮어씀
# index=False: DataFrame 인덱스는 저장하지 않음, dtype: 컬럼별 자료형 지정
df.to_sql(name='dept_df', con=conn, if_exists='replace', index=False,
          dtype={'DEPTNO': 'integer', 'DNAME': 'text', 'LOC': 'text'})

# emp 테이블 생성 (dtype 생략 시 pandas가 자료형을 자동 지정)
df = pd.read_csv(DATA_DIR / 'emp.csv')
df.to_sql(name='emp_df', con=conn, if_exists='replace', index=False)

conn.close()  # DB 연결 종료
