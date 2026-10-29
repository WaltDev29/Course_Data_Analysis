# ==============================================================================
# 과제: 수원시 장안구 무인교통단속카메라 데이터 분석 및 지도 시각화
# ==============================================================================

import os
from pathlib import Path
import re
import folium
from folium.plugins import HeatMap, MarkerCluster
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# display_map 모듈 import
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import display_map as dm

# 한글 폰트 및 스타일 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
sns.set_theme(style='whitegrid', font='Malgun Gothic')

# ------------------------------------------------------------------------------
# 1. 전국 파일에서 본인 수원시 장안구만 추출하고, 카메라 수와 제공기관별 수를 보이시오.
# ------------------------------------------------------------------------------
DATA_DIR = Path(__file__).resolve().parents[1] / 'data'
df_raw = pd.read_csv(DATA_DIR / 'traffic_cam.csv', encoding='cp949')

# 수원시 장안구 필터링 (경기도 수원시 내 지번/도로명 주소에 '장안구' 포함)
cond_jangan = (df_raw['시도명'] == '경기도') & (
    df_raw['소재지도로명주소'].str.contains('장안구', na=False) |
    df_raw['소재지지번주소'].str.contains('장안구', na=False)
)
df_jangan = df_raw[cond_jangan].copy().reset_index(drop=True)

print("=" * 65)
print("1. 수원시 장안구 카메라 추출 및 제공기관별 수")
print("=" * 65)
print(f"▶ 수원시 장안구 총 카메라 수: {len(df_jangan)}대\n")
print("▶ 제공기관별 카메라 수:")
agency_counts = df_jangan['제공기관명'].value_counts()
print(agency_counts.to_string())

# ------------------------------------------------------------------------------
# 2. 단속구분 표기를 통일하여 단속유형 · 보호구역 컬럼을 만들고 각각의 개수를 보이시오.
# ------------------------------------------------------------------------------
# 단속구분 코드 표준화 매핑 (1: 과속, 2: 신호, 4: 주정차, 99: 기타)
def map_enforcement_type(val):
    val_str = str(val).strip()
    if val_str in ['1', '01']:
        return '과속'
    elif val_str in ['2', '02']:
        return '신호'
    elif val_str in ['3', '03']:
        return '통행위반'
    elif val_str in ['4', '04']:
        return '주정차'
    elif val_str in ['1+2', '01+02']:
        return '신호/과속'
    else:
        return '기타'

# 보호구역구분 코드 표준화 매핑 (1: 노인보호구역, 2: 어린이보호구역, 99/NaN: 해당없음)
def map_protection_zone(val):
    if pd.isna(val):
        return '해당없음'
    try:
        val_int = int(float(val))
    except (ValueError, TypeError):
        return '해당없음'
        
    if val_int == 1:
        return '노인보호구역'
    elif val_int == 2:
        return '어린이보호구역'
    elif val_int == 3:
        return '장애인보호구역'
    else:
        return '해당없음'

df_jangan['단속유형'] = df_jangan['단속구분'].apply(map_enforcement_type)
df_jangan['보호구역'] = df_jangan['보호구역구분'].apply(map_protection_zone)

print("\n" + "=" * 65)
print("2. 단속유형 및 보호구역 컬럼 생성 및 개수")
print("=" * 65)
print("▶ 단속유형별 개수:")
print(df_jangan['단속유형'].value_counts().to_string())
print("\n▶ 보호구역별 개수:")
print(df_jangan['보호구역'].value_counts().to_string())

# ------------------------------------------------------------------------------
# 3. 어린이보호구역 카메라만 MarkerCluster로 표시 (팝업: 설치장소, 단속유형, 제한속도, 설치연도)
# 4. 단속유형별 FeatureGroup 레이어를 만들고, 배경 지도를 2개 이상 고를 수 있게 하시오.
# 5. HeatMap을 그리고, 카메라가 가장 많은 동 · 읍 · 면 3곳을 쓰시오.
# ------------------------------------------------------------------------------
# 지도의 중심 좌표 계산 (장안구 전체 카메라의 위도/경도 평균)
center = [df_jangan['위도'].mean(), df_jangan['경도'].mean()]

# 배경 지도를 전환할 수 있도록 tiles=None으로 기본 맵 생성
traffic_map = folium.Map(location=center, zoom_start=13, tiles=None)

# 배경 지도 3종 추가 (배경 지도를 2개 이상 선택 가능: OSM HOT, Google 로드맵, Google 위성)
folium.TileLayer('OpenStreetMap.HOT', name='OpenStreetMap (HOT)').add_to(traffic_map)
folium.TileLayer('https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', attr='Google', name='Google 로드맵').add_to(traffic_map)
folium.TileLayer('https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google', name='Google 위성(하이브리드)').add_to(traffic_map)

# [5번] HeatMap 레이어 생성 및 추가
heat_data = df_jangan[['위도', '경도']].dropna().values.tolist()
fg_heatmap = folium.FeatureGroup(name='🔥 단속카메라 밀집도 (HeatMap)', show=True)
HeatMap(heat_data, radius=18, blur=14, min_opacity=0.35).add_to(fg_heatmap)
fg_heatmap.add_to(traffic_map)

# [3번] 어린이보호구역 카메라 MarkerCluster 레이어 생성
# ※ 사거리 등 초근접/동일 좌표 마커 클릭 시 방사형 분리(spiderfy) 및 확대 시 클러스터 해제 옵션 적용
df_child = df_jangan[df_jangan['보호구역'] == '어린이보호구역'].copy().reset_index(drop=True)
cluster_child = MarkerCluster(
    name='★ 어린이보호구역 카메라 (MarkerCluster)',
    spiderfyOnMaxZoom=True,        # 최대 확대 시 방사형으로 펼침 (사거리 초밀집/중복 좌표 마커 분리)
    disableClusteringAtZoom=17,    # 줌 레벨 17 이상부터는 클러스터 강제 해제하여 개별 마커 직접 노출
    maxClusterRadius=35            # 클러스터 결합 반경을 줄여 조금만 확대해도 분리되도록 설정
).add_to(traffic_map)

for _, row in df_child.iterrows():
    install_year = f"{int(row['설치연도'])}년" if pd.notna(row['설치연도']) else "정보 없음"
    speed_limit = f"{int(row['제한속도'])} km/h" if pd.notna(row['제한속도']) and row['제한속도'] > 0 else "제한속도 없음"
    
    popup_html = f"""
    <div style="font-family:'Malgun Gothic',sans-serif; width:220px; font-size:12px; line-height:1.6;">
        <h4 style="margin:0 0 6px 0; color:#d90429; border-bottom:1px solid #ddd; padding-bottom:4px;">
            어린이보호구역 단속카메라
        </h4>
        <b>설치장소:</b> {row['설치장소']}<br>
        <b>단속유형:</b> {row['단속유형']}<br>
        <b>제한속도:</b> {speed_limit}<br>
        <b>설치연도:</b> {install_year}
    </div>
    """
    folium.Marker(
        location=[row['위도'], row['경도']],
        popup=folium.Popup(popup_html, max_width=260),
        tooltip=f"[어린이보호구역] {row['설치장소']}",
        icon=folium.Icon(color='orange', icon='child', prefix='fa')
    ).add_to(cluster_child)

# [4번] 단속유형별 FeatureGroup 레이어 생성
type_styles = {
    '신호': {'color': 'red', 'icon': 'exclamation-circle'},
    '과속': {'color': 'blue', 'icon': 'tachometer', 'prefix': 'fa'},
    '기타': {'color': 'purple', 'icon': 'info-circle', 'prefix': 'fa'}
}

for type_name in df_jangan['단속유형'].unique():
    fg = folium.FeatureGroup(name=f"단속유형: {type_name}단속")
    df_type = df_jangan[df_jangan['단속유형'] == type_name]
    style = type_styles.get(type_name, {'color': 'gray', 'icon': 'camera'})
    
    for _, row in df_type.iterrows():
        install_year = f"{int(row['설치연도'])}년" if pd.notna(row['설치연도']) else "정보 없음"
        speed_limit = f"{int(row['제한속도'])} km/h" if pd.notna(row['제한속도']) and row['제한속도'] > 0 else "제한속도 없음"
        
        popup_html = f"""
        <div style="font-family:'Malgun Gothic',sans-serif; width:220px; font-size:12px; line-height:1.6;">
            <h4 style="margin:0 0 6px 0; color:#1d3557; border-bottom:1px solid #ddd; padding-bottom:4px;">
                무인교통단속카메라 ({type_name})
            </h4>
            <b>설치장소:</b> {row['설치장소']}<br>
            <b>보호구역:</b> {row['보호구역']}<br>
            <b>제한속도:</b> {speed_limit}<br>
            <b>설치연도:</b> {install_year}
        </div>
        """
        prefix = style.get('prefix', 'glyphicon')
        folium.Marker(
            location=[row['위도'], row['경도']],
            popup=folium.Popup(popup_html, max_width=260),
            tooltip=f"[{type_name}] {row['설치장소']}",
            icon=folium.Icon(color=style['color'], icon=style['icon'], prefix=prefix)
        ).add_to(fg)
        
    fg.add_to(traffic_map)

# 레이어 컨트롤 추가 (배경 지도 선택 라디오 버튼 및 오버레이 레이어 체크박스 활성화)
folium.LayerControl(collapsed=False).add_to(traffic_map)

# 지도 브라우저 표시
dm.showMap(traffic_map)

# ------------------------------------------------------------------------------
# 5번 추가 분석: 카메라가 가장 많은 동 · 읍 · 면 3곳 분석
# ------------------------------------------------------------------------------
# 지번주소, 도로명주소, 설치장소 등에서 '동' 단위 추출
def extract_dong(row):
    addr_jibun = str(row['소재지지번주소']) if pd.notna(row['소재지지번주소']) else ''
    addr_doro = str(row['소재지도로명주소']) if pd.notna(row['소재지도로명주소']) else ''
    full_text = f"{addr_jibun} {addr_doro} {row['설치장소']}"
    
    # 대표 법정동 우선 매칭
    known_dongs = ['정자동', '조원동', '천천동', '율전동', '영화동', '파장동', '연무동', '하광교동', '상광교동', '송죽동', '이목동']
    for dong in known_dongs:
        if dong in full_text:
            return dong
            
    m = re.search(r'([가-힣]+동)', full_text)
    if m:
        return m.group(1)
    return '기타'

df_jangan['동'] = df_jangan.apply(extract_dong, axis=1)
dong_counts = df_jangan['동'].value_counts()
top3_dongs = dong_counts.head(3)

print("\n" + "=" * 65)
print("5. HeatMap 생성 및 카메라 최다 설치 동 3곳")
print("=" * 65)
print("▶ 장안구 전체 동별 단속카메라 설치 현황:")
print(dong_counts.to_string())
print("\n▶ 카메라가 가장 많은 동 3곳:")
for rank, (dong, count) in enumerate(top3_dongs.items(), 1):
    print(f"  {rank}위: {dong} ({count}대)")

# ------------------------------------------------------------------------------
# 6. 심화 분석: 
#   [주제 1] 동별 단속카메라 설치 대수 및 단속유형(신호 vs 과속) 분포
#   [주제 3] 제공기관(경찰청 vs 수원시)별 역할 분담 및 단속/보호구역 비교
# ------------------------------------------------------------------------------
print("\n" + "=" * 65)
print("6. 심화 데이터 분석 (주제 1 & 주제 3)")
print("=" * 65)

# [주제 1 분석] 동별 단속유형 교차 집계
dong_type_ct = pd.crosstab(df_jangan['동'], df_jangan['단속유형'])
dong_type_ct['총계'] = dong_type_ct.sum(axis=1)
dong_type_ct = dong_type_ct.sort_values(by='총계', ascending=True)  # 수평 막대그래프를 위해 오름차순 정렬
plot_dong_ct = dong_type_ct.drop(columns='총계')

print("▶ [주제 1] 동별 단속유형(신호 vs 과속) 설치 현황:")
print(dong_type_ct[['신호', '과속', '총계']].sort_values(by='총계', ascending=False).to_string())

# [주제 3 분석] 제공기관별 보호구역 및 단속유형 교차 집계
agency_prot_ct = pd.crosstab(df_jangan['제공기관명'], df_jangan['보호구역'])
agency_type_ct = pd.crosstab(df_jangan['제공기관명'], df_jangan['단속유형'])

print("\n▶ [주제 3] 제공기관별 보호구역 및 단속유형 분포:")
print("[보호구역 구분]")
print(agency_prot_ct.to_string())
print("\n[단속유형 구분]")
print(agency_type_ct.to_string())

# 서브플롯(1행 2열) 시각화 생성
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

# ------------------------------------------------------------------------------
# 그래프 1: [주제 1] 동별 단속카메라 설치 대수 및 단속유형(신호 vs 과속) 수평 누적 막대그래프
# ------------------------------------------------------------------------------
colors = {'신호': '#e63946', '과속': '#457b9d', '기타': '#6c757d'}
bottom = np.zeros(len(plot_dong_ct))

for col in ['신호', '과속', '기타']:
    if col in plot_dong_ct.columns:
        values = plot_dong_ct[col].values
        ax1.barh(plot_dong_ct.index, values, left=bottom, label=f"{col}단속", color=colors.get(col, '#999'), height=0.65)
        bottom += values

# 총합 텍스트 표시
for idx, (dong, total) in enumerate(dong_type_ct['총계'].items()):
    ax1.text(total + 0.8, idx, f"{total}대", va='center', fontsize=10, fontweight='bold', color='#2b2d42')

ax1.set_title("수원시 장안구 동별 단속카메라 대수 및 단속유형(신호 vs 과속)", fontsize=13, fontweight='bold', pad=12)
ax1.set_xlabel("설치 대수 (대)", fontsize=11)
ax1.set_ylabel("동(洞)", fontsize=11)
ax1.set_xlim(0, dong_type_ct['총계'].max() + 6)
ax1.legend(loc='lower right', frameon=True)
ax1.grid(axis='x', linestyle='--', alpha=0.7)

# ------------------------------------------------------------------------------
# 그래프 2: [주제 3] 제공기관(경찰청 vs 수원시)별 보호구역 및 단속유형 비교 그룹 막대그래프
# ------------------------------------------------------------------------------
agencies = agency_prot_ct.index.tolist()
x = np.arange(len(agencies))
width = 0.22

# 지표 구성: 어린이보호구역, 일반구역, 신호단속, 과속단속
child_vals = [agency_prot_ct.loc[ag, '어린이보호구역'] if '어린이보호구역' in agency_prot_ct.columns else 0 for ag in agencies]
gen_vals = [agency_prot_ct.loc[ag, '해당없음'] if '해당없음' in agency_prot_ct.columns else 0 for ag in agencies]
signal_vals = [agency_type_ct.loc[ag, '신호'] if '신호' in agency_type_ct.columns else 0 for ag in agencies]
speed_vals = [agency_type_ct.loc[ag, '과속'] if '과속' in agency_type_ct.columns else 0 for ag in agencies]

rects1 = ax2.bar(x - width * 1.5, child_vals, width, label='어린이보호구역', color='#ffb703')
rects2 = ax2.bar(x - width * 0.5, gen_vals, width, label='일반구역', color='#8ecae6')
rects3 = ax2.bar(x + width * 0.5, signal_vals, width, label='신호단속', color='#d90429')
rects4 = ax2.bar(x + width * 1.5, speed_vals, width, label='과속단속', color='#1d3557')

# 막대 위 수치 라벨 표시
for rects in [rects1, rects2, rects3, rects4]:
    for bar in rects:
        h = bar.get_height()
        if h > 0:
            ax2.text(bar.get_x() + bar.get_width() / 2., h + 1, f"{int(h)}대", ha='center', va='bottom', fontsize=9, fontweight='bold')

ax2.set_title("제공기관(경찰청 vs 수원시)별 보호구역 및 단속유형 역할 분담", fontsize=13, fontweight='bold', pad=12)
ax2.set_xticks(x)
ax2.set_xticklabels(agencies, fontsize=11, fontweight='bold')
ax2.set_ylabel("카메라 대수 (대)", fontsize=11)
ax2.set_ylim(0, max(child_vals + signal_vals) + 12)
ax2.legend(loc='upper right', frameon=True)
ax2.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()

# ------------------------------------------------------------------------------
# 분석 결과 텍스트 출력
# ------------------------------------------------------------------------------
summary_text = """
=================================================================
[분석 인사이트 요약]
=================================================================
1. [주제 1: 동별 설치 특성]
   - 정자동(48대), 조원동(20대), 천천동(20대) 등 대규모 주거단지와 초등학교, 학원가가
     밀집한 지역에 단속카메라가 집중 배치되어 있습니다.
   - 특히 정자동과 천천동은 '신호단속' 카메라의 비중이 70~80%에 달해, 보행자 횡단보도
     안전을 위한 신호위반 단속 위주로 인프라가 구축되어 있음을 알 수 있습니다.

2. [주제 3: 제공기관별 역할 분담]
   - 경찰청(83대)과 경기도 수원시(72대)는 긴밀한 역할 분담을 보이고 있습니다.
   - 어린이보호구역 단속카메라는 수원시(47대)와 경찰청(48대)이 균형 있게 공동 투자하였으며,
   - 전체적으로 보행자 보호 목적의 '신호단속(수원시 54대, 경찰청 62대)'이 '과속단속'보다
     3배 이상 많이 설치되어 있어 도심 보행자 안전을 최우선으로 관리하고 있습니다.
=================================================================
"""
print(summary_text)
