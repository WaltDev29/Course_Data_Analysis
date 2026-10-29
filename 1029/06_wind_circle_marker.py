# 풍속 측정 위치를 마커로, 풍속 크기를 원의 크기로 지도에 표시하는 예제
import folium  # 지도 시각화 라이브러리

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))    # 이 파일(display_map.py와 같은 폴더)이 있는 폴더로 이동
import display_map as dm  # 지도를 웹 브라우저에 띄우는 사용자 정의 모듈
import pandas as pd  # 데이터 처리 라이브러리
from pathlib import Path  # 파일 경로 처리용

# 이 파일의 위치를 기준으로 데이터 폴더를 찾는다(어느 폴더에서 실행해도 동작)
DATA_DIR = Path(__file__).resolve().parents[1] / 'data'

df = pd.read_csv(DATA_DIR / 'wind.csv')  # 풍속 측정 데이터 읽기(lat: 위도, lon: 경도, spd: 풍속)
print(df.head())  # 앞 5행 확인

df = df.sample(50, random_state=123)  # 50개 행만 무작위 추출(random_state: 매번 같은 결과)

# 지도의 중심점 구하기
center = [df.lat.mean(), df.lon.mean()]  # 위도·경도의 평균

# 지도 가져오기
# 기본 OpenStreetMap 타일은 로컬 html(file://)에서 차단(403)되므로 OSM HOT 타일(같은 OSM 데이터, 프랑스 서버)을 사용한다
map = folium.Map(location=center, zoom_start=5, tiles='OpenStreetMap.HOT')  # 지도 객체 생성
dm.showMap(map)  # 웹 브라우저에 지도 표시

# 측정 위치에 마커 표시하기
for i in range(len(df)):  # 측정 위치 수만큼 반복
    folium.Marker(location=[df.lat.iloc[i], df.lon.iloc[i]],  # i번째 위치의 위도, 경도
                  icon=folium.Icon(color='blue', icon='flag')).add_to(map)  # 파란색 깃발 아이콘
# dm.showMap(map)  # 웹 브라우저에 지도 표시

# 풍속을 원의 크기로 표시하기
# map = folium.Map(location=center, zoom_start=5, tiles='OpenStreetMap.HOT')  # 마커 없는 지도

for i in range(len(df)):  # 측정 위치 수만큼 반복
    folium.CircleMarker(location=[df.lat.iloc[i], df.lon.iloc[i]],
                        radius=(df.spd.iloc[i]**0.5)*2,  # 원의 반지름
                        color='red',  # 원의 색
                        stroke=False,  # 윤곽선 없음
                        fill=True,  # 원의 내부 색
                        fill_opacity='50%'  # 원의 내부 색 투명도
                        ).add_to(map)
dm.showMap(map)  # 웹 브라우저에 지도 표시
