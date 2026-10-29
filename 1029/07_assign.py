# ==============================================================================
# 과제: 지하철 2호선 역별 오전 8~9시대 탑승객 수 지도 시각화
# ==============================================================================

import os
from pathlib import Path
import folium
import geokakao as gk
import pandas as pd

# display_map 모듈 import (현재 스크립트 실행 위치 기준)
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import display_map as dm

# ------------------------------------------------------------------------------
# 1. 지하철 탑승객 데이터셋과 지하철역 주소 데이터를 읽는다.
# ------------------------------------------------------------------------------
DATA_DIR = Path(__file__).resolve().parents[1] / 'data'

df_subway = pd.read_csv(DATA_DIR / 'subway_line_1_8_20231231.csv')
df_addr = pd.read_csv(DATA_DIR / 'seoul_subway_address_2023.csv')

# ------------------------------------------------------------------------------
# 2. 지하철 탑승객 데이터셋에서 2호선의 오전 8~9시대 탑승객 수를 역별로 집계한다.
# ------------------------------------------------------------------------------
# 2호선이면서 '승차' 데이터만 필터링
df_line2 = df_subway[(df_subway['호선명'] == 2) & (df_subway['승하차구분'] == '승차')]

# 역별 8~9시대 탑승객 수 합계 집계
df_passenger = df_line2.groupby(['역번호', '역명'])['t08_09시간대'].sum().reset_index()
df_passenger.rename(columns={'t08_09시간대': '탑승객수'}, inplace=True)
print("=== 2호선 역별 오전 8~9시 탑승객 집계 (상위 5개) ===")
print(df_passenger.sort_values(by='탑승객수', ascending=False).head())

# ------------------------------------------------------------------------------
# 3. 탑승객 데이터와 역 주소 데이터를 병합한 뒤, 주소를 이용해 위도와 경도 값을 추가한다.
# ------------------------------------------------------------------------------
# 2호선 주소 데이터 (역번호 기준)
df_addr_line2 = df_addr[df_addr['호선'] == 2][['역번호', '도로명주소']].copy()

# 역번호 기준으로 탑승객 데이터와 주소 데이터 병합
df_merged = pd.merge(df_passenger, df_addr_line2, on='역번호', how='inner')

# 카카오 API를 활용해 도로명주소로 위도(decimalLatitude), 경도(decimalLongitude) 컬럼 추가
gk.add_coordinates_to_dataframe(df_merged, '도로명주소')

# 위도와 경도를 숫자형(float)으로 변환
df_merged['decimalLatitude'] = pd.to_numeric(df_merged['decimalLatitude'])
df_merged['decimalLongitude'] = pd.to_numeric(df_merged['decimalLongitude'])
print("\n=== 병합 및 좌표 추가 결과 (상위 5개) ===")
print(df_merged[['역명', '도로명주소', 'decimalLatitude', 'decimalLongitude', '탑승객수']].head())

# ------------------------------------------------------------------------------
# 4. 지도의 중심점을 계산한다.
# ------------------------------------------------------------------------------
center = [df_merged['decimalLatitude'].mean(), df_merged['decimalLongitude'].mean()]
print(f"\n지도의 중심 좌표: {center}")

# 지도 객체 생성 (로컬 환경에서 403 에러 없는 OSM HOT 타일 사용)
subway_map = folium.Map(location=center, zoom_start=12, tiles='OpenStreetMap.HOT')

# ------------------------------------------------------------------------------
# 5. 역의 위치를 지도 위에 마커로 표시한다.
# 6. 역별 탑승객 수를 역의 위치에 원으로 표시하고, 역 이름도 함께 나타낸다.
# ------------------------------------------------------------------------------
# 역 이름 표시용 HTML 태그 스타일
html_start = (
    '<div style="'
    'font-size: 11px;'
    'color: #1b4332;'
    'font-weight: bold;'
    'background-color: rgba(255, 255, 255, 0.85);'
    'border: 1px solid #2d6a4f;'
    'border-radius: 4px;'
    'padding: 2px 4px;'
    'white-space: nowrap;'
    'width: max-content;'
    'text-align: center;'
    'margin: 0px;'
    'box-shadow: 1px 1px 2px rgba(0,0,0,0.2);'
    '">'
)
html_end = '</div>'

for i in range(len(df_merged)):
    lat = df_merged.loc[i, 'decimalLatitude']
    lon = df_merged.loc[i, 'decimalLongitude']
    name = df_merged.loc[i, '역명']
    count = df_merged.loc[i, '탑승객수']

    # 5. 역의 위치를 지도 위에 마커로 표시
    folium.Marker(
        location=[lat, lon],
        popup=f"<b>{name}역 (2호선)</b><br>오전 8~9시 탑승객: {count:,}명",
        tooltip=f"{name}역",
        icon=folium.Icon(color='green', icon='info-sign')
    ).add_to(subway_map)

    # 6-1. 역별 탑승객 수를 원(CircleMarker)으로 표시 (반지름은 탑승객 수 제곱근에 비례하도록 스케일링)
    radius = (count ** 0.5) / 35
    folium.CircleMarker(
        location=[lat, lon],
        radius=radius,
        color="red",
        stroke=False,
        weight=1.5,
        fill=True,
        fill_opacity=0.5
    ).add_to(subway_map)

    # 6-2. 역 이름을 텍스트(DivIcon)로 함께 나타냄
    folium.Marker(
        location=[lat, lon],
        icon=folium.DivIcon(
            icon_anchor=(-10, 15),  # 마커 오른쪽 약간 아래에 텍스트 배치
            html=html_start + name + html_end
        )
    ).add_to(subway_map)

# ------------------------------------------------------------------------------
# 웹 브라우저로 지도 표시
# ------------------------------------------------------------------------------
dm.showMap(subway_map)
print("\n지하철 2호선 역별 탑승객 시각화 지도가 성공적으로 생성되어 브라우저에 표시되었습니다.")
