# 마커 위치에 HTML 텍스트(장소 이름)를 함께 표시하는 예제
import folium  # 지도 시각화 라이브러리
import geokakao as gk  # 카카오 API로 주소를 좌표로 변환하는 라이브러리

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))    # 이 파일(display_map.py와 같은 폴더)이 있는 폴더로 이동
import display_map as dm  # 지도를 웹 브라우저에 띄우는 사용자 정의 모듈

loc = gk.convert_address_to_coordinates('강원특별자치도 강릉시 창해로 514')  # 경포해수욕장 주소 → [위도, 경도]
print(loc)  # 변환된 좌표 확인
# 기본 OpenStreetMap 타일은 로컬 html(file://)에서 차단(403)되므로 OSM HOT 타일(같은 OSM 데이터, 프랑스 서버)을 사용한다
map = folium.Map(location=loc, zoom_start=13, tiles='OpenStreetMap.HOT')  # 지도 객체 생성
folium.Marker(location=loc,  # 마커 표시
              icon=folium.Icon(color='red', icon='star')).add_to(map)  # 빨간색 별 모양 아이콘
dm.showMap(map)  # 웹 브라우저에 지도 표시

# 마커 위치에 텍스트 추가
# 텍스트 앞부분: 글자 크기·색·반투명 배경 등 스타일을 지정한 HTML 태그
html_start = html = '<div \
style="\
font-size: 12px;\
color: blue;\
background-color:rgba(255, 255, 255, 0.2);\
width:85px;\
text-align:left;\
margin:0px;\
"><b>'
html_end = '</b></div>'  # 텍스트 뒷부분: 열었던 태그 닫기

folium.Marker(location=loc,
              icon=folium.DivIcon(  # 아이콘 대신 HTML을 표시하는 마커
                  icon_anchor=(0, 0),  # 텍스트 위치 설정
                  html=html_start+'경포해수욕장'+html_end  # 표시할 HTML(스타일+텍스트)
              )).add_to(map)

dm.showMap(map)  # 웹 브라우저에 지도 표시
