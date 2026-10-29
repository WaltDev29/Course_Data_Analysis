# 여러 관광지 주소를 좌표로 바꿔 마커와 이름을 지도에 표시하는 예제
import folium  # 지도 시각화 라이브러리
import geokakao as gk  # 카카오 API로 주소를 좌표로 변환하는 라이브러리

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))    # 이 파일(display_map.py와 같은 폴더)이 있는 폴더로 이동
import display_map as dm  # 지도를 웹 브라우저에 띄우는 사용자 정의 모듈
import pandas as pd  # 데이터 처리 라이브러리

# 관광지 정보를 데이터프레임으로 저장
names = ['용두암', '성산일출봉', '정방폭포',
         '중문관광단지', '한라산1100고지', '차귀도']  # 관광지 이름
addr = ['제주시 용두암길 15',
        '서귀포시 성산읍 성산리',
        '서귀포시 동홍동 299-3',
        '서귀포시 중문동 2624-1',
        '서귀포시 색달동 산1-2',
        '제주시 한경면 고산리 산 117']  # 관광지 주소

dict = {"names": names, "addr": addr}  # 컬럼 이름: 값 리스트
df = pd.DataFrame(dict)  # 데이터프레임 생성
print(df)  # 데이터 확인

# 관광지의 좌표를 df에 추가
gk.add_coordinates_to_dataframe(df, 'addr')  # addr 컬럼 주소로 decimalLatitude, decimalLongitude 컬럼 추가
print(df)  # 좌표 컬럼 추가 확인
print(df.dtypes)  # 컬럼 자료형 확인(좌표가 문자열로 들어옴)

# 문자열 좌푯값을 숫자로 변환
df.decimalLatitude = pd.to_numeric(df.decimalLatitude)  # 위도
df.decimalLongitude = pd.to_numeric(df.decimalLongitude)  # 경도
print(df.dtypes)  # 숫자형으로 바뀌었는지 확인

# 지도의 중심점 계산
center = [df.decimalLatitude.mean(), df.decimalLongitude.mean()]  # 관광지 위도·경도의 평균
print(center)  # 중심 좌표 확인

# 지도 객체 생성
# 기본 OpenStreetMap 타일은 로컬 html(file://)에서 차단(403)되므로 OSM HOT 타일(같은 OSM 데이터, 프랑스 서버)을 사용한다
map = folium.Map(location=center, zoom_start=10, tiles='OpenStreetMap.HOT')

# 지도에 마커 추가
for i in range(len(df)):  # 관광지 수만큼 반복
    folium.Marker(location=[df.iloc[i, 2], df.iloc[i, 3]],  # 2번 열: 위도, 3번 열: 경도                
                  icon=folium.Icon(color='red', icon='star')).add_to(map)  # 빨간색 별 모양 아이콘
dm.showMap(map)  # 웹 브라우저에 지도 표시

# 지도에 텍스트(관광지명) 추가
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

for i in range(len(df)):  # 관광지 수만큼 반복
    folium.Marker(location=[df.iloc[i, 2], df.iloc[i, 3]],
              icon=folium.DivIcon(  # 아이콘 대신 HTML을 표시하는 마커
                  icon_anchor=(0, 0),  # 텍스트 위치 설정
                  html=html_start+df.names[i]+html_end  # 관광지 이름을 HTML로 표시
                  )).add_to(map)

# 웹 브라우저에 지도 출력
dm.showMap(map)