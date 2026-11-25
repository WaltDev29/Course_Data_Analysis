# SQLite DB 연결·질의·종료를 묶어 둔 사용자 정의 클래스 (다른 예제에서 import 해서 사용)

import sqlite3          # 파이썬 내장 SQLite 모듈
import pandas as pd     # 질의 결과를 DataFrame으로 만들기 위해 사용
from pathlib import Path

# 이 파일의 위치를 기준으로 데이터 폴더를 찾는다(어느 폴더에서 실행해도 동작)
# parents[0]=Ch13, parents[1]=src, parents[2]=source → source/data 폴더
DATA_DIR = Path(__file__).resolve().parents[1] / 'data'

class SQLite:
    # 객체를 만들 때 DB에 연결하고 커서를 준비한다 (기본 DB는 emp.db)
    def __init__(self, db_path=DATA_DIR / 'emp.db'):
        self.conn = sqlite3.connect(db_path)   # DB 연결 객체 (파일이 없으면 새로 생성됨)
        self.cur = self.conn.cursor()          # SQL을 실행할 커서 객체

    def close_db(self):  # 커서와 DB 연결 종료
        self.cur.close()
        self.conn.close()

    def run_sql(self, sql):  # SQL 문 실행
        self.cur.execute(sql)                  # SQL 실행
        result = self.cur.fetchall()           # 결과 행 전체를 튜플의 리스트로 가져옴
        # cur.description 의 각 항목 첫 번째 값이 컬럼 이름
        columns = [column[0] for column in self.cur.description]
        df_result = pd.DataFrame(result, columns=columns)  # 결과를 표 형태로 변환
        return df_result
