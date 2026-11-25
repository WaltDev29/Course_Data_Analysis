# 서울 지하철 승하차 CSV를 SQLite 클래스로 DB에 subway 테이블로 저장하는 예제

import os
from pathlib import Path
# 이 파일이 있는 폴더(Ch13)로 이동 → 같은 폴더의 SQLite.py 를 불러올 수 있음
os.chdir(Path(__file__).resolve().parent)

from SQLite import *     # SQLite.py 의 SQLite 클래스 불러오기
import pandas as pd

# 이 파일의 위치를 기준으로 데이터 폴더를 찾는다(어느 폴더에서 실행해도 동작)
DATA_DIR = Path(__file__).resolve().parents[1] / 'data'

SL = SQLite()                     # emp.db 에 연결

# subway 테이블 생성
df = pd.read_csv(DATA_DIR / 'subway_line_1_8_20231231.csv')
# SL.conn: SQLite 객체가 가진 DB 연결을 그대로 to_sql()에 넘김
df.to_sql('subway', con=SL.conn, if_exists='replace', index=False)

SL.close_db()  # DB 작업 종료
