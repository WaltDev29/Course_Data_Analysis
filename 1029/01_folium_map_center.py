# 좌표 또는 주소로 지도의 중심을 정해 folium 지도를 표시하는 예제
import folium  # 지도 시각화 라이브러리
import geokakao as gk  # 카카오 API로 주소를 좌표로 변환하는 라이브러리

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))    # 이 파일(display_map.py와 같은 폴더)이 있는 폴더로 이동
import display_map as dm  # 지도를 웹 브라우저에 띄우는 사용자 정의 모듈

# 지도 중심의 좌표를 알 때
loc = [37.54, 127.05]  # 위도, 경도
# 기본 OpenStreetMap 타일은 로컬 html(file://)에서 차단(403)되므로 OSM HOT 타일(같은 OSM 데이터, 프랑스 서버)을 사용한다
map = folium.Map(location=loc, tiles='OpenStreetMap.HOT')  # 지도 객체 생성
dm.showMap(map)  # 웹 브라우저에 지도 표시

# 지도 중심의 주소를 알 때
loc = gk.convert_address_to_coordinates('경기 용인시 수지구 죽전로 152')  # 주소 → [위도, 경도]
print(loc)  # 지도의 중심 좌표
#map = folium.Map(center=loc, zoom_start=16)  # 지도 객체 생성
map = folium.Map(location=loc, zoom_start=16, tiles='OpenStreetMap.HOT')  # 지도 객체 생성(zoom_start: 확대 정도, 클수록 자세히)
dm.showMap(map)  # 웹 브라우저에 지도 표시