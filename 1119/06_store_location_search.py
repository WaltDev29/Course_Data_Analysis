# 상가 정보를 DB에 저장한 뒤 특정 주소(강남역) 주변 상가를 위도·경도 범위로 검색하는 실전 분석 예제

import geokakao as gk     # 카카오 API로 주소를 위도·경도 좌표로 변환하는 패키지
import pandas as pd

import os
os.chdir('d:/ds_study/Ch13/')     # SQLite.py 가 있는 폴더 지정
from SQLite import *
from pathlib import Path

# 이 파일의 위치를 기준으로 데이터 폴더를 찾는다(어느 폴더에서 실행해도 동작)
DATA_DIR = Path(__file__).resolve().parents[1] / 'data'

SL = SQLite()

# store 테이블 생성 (서울시 상가 정보 CSV → DB 테이블)
df = pd.read_csv(DATA_DIR / 'seoul_201712.csv')
df.to_sql('store', con=SL.conn, if_exists='replace', index=False)

# rowid: SQLite가 행마다 자동으로 붙이는 번호 → 앞 10행만 조회
sql = 'select * from store where rowid <= 10'
print(SL.run_sql(sql))  # 질의 결과 확인

# 강남역 주소를 위도·경도로 변환 (결과는 [위도, 경도] 문자열)
addr = '서울특별시 강남구 강남대로 지하396'
lat_lon = gk.convert_address_to_coordinates(addr)
lat_lon = [float(lat_lon[0]), float(lat_lon[1])]  # 문자열을 숫자로 변환

# 기준 좌표에서 위도·경도 ±0.001(약 100m) 범위 안의 상가 이름과 업종 조회
# format()으로 {} 자리에 범위 값을 차례로 채워 넣음
sql = "select store_name, class_small from store \
    where lat between {} and {} \
        and lon between {} and {}".format(lat_lon[0]-0.001, lat_lon[0]+0.001,
                                          lat_lon[1]-0.001, lat_lon[1]+0.001)

result = SL.run_sql(sql)  # 질의 결과 확인
result.info()             # 행 수와 컬럼 정보 확인
print(result.head())

# 검색 결과를 CSV로 저장
result.to_csv('d:/ds_study/store_info.csv', encoding='EUC-KR')

SL.close_db()  # DB 작업 종료
