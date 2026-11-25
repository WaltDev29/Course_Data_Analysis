# -*- coding: utf-8 -*-
"""
과제: 주민등록 인구통계(jumin.csv) 데이터를 활용한 주성분 분석(PCA) 및 시각화
1. 데이터 전처리: 쉼표(,) 제거 및 수치형 변환, 행정표준코드를 이용한 지역명 복원, 전국 합계 행 제외
2. 데이터 표준화(StandardScaler): 단위가 다른 인구 통계 변수 표준화
3. 주성분 분석(PCA): 2차원 축소 및 설명 분산 비율 산출
4. 결과 시각화: 지역별 PCA 2차원 산점도 및 주성분 기여도(Loading) 시각화
"""

import re
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from matplotlib import font_manager

# ---------------------------------------------------------
# 0. 한글 폰트 설정 및 경로 지정
# ---------------------------------------------------------
installed_fonts = {f.name for f in font_manager.fontManager.ttflist}
font_name = next((f for f in ['Malgun Gothic', 'AppleGothic', 'NanumGothic', 'Noto Sans CJK KR'] if f in installed_fonts), None)
if font_name:
    plt.rcParams['font.family'] = font_name
plt.rcParams['axes.unicode_minus'] = False

# 이 파일의 위치를 기준으로 데이터 폴더를 찾음 (data/jumin.csv)
DATA_DIR = Path(__file__).resolve().parents[1] / 'data'
DATA_PATH = DATA_DIR / 'jumin.csv'

# ---------------------------------------------------------
# 1. 데이터 불러오기 및 전처리
# ---------------------------------------------------------
df = pd.read_csv(DATA_PATH, encoding='utf-8')

# 행정표준코드(10자리) 매핑 사전 (깨진 행정구역 텍스트 완벽 복원)
code_to_region = {
    '1000000000': '전국',
    '1100000000': '서울특별시',
    '1200000000': '세종특별자치시',
    '2600000000': '부산광역시',
    '2700000000': '대구광역시',
    '2800000000': '인천광역시',
    '2900000000': '광주광역시',
    '3000000000': '대전광역시',
    '3100000000': '울산광역시',
    '3600000000': '세종특별자치시',
    '4100000000': '경기도',
    '5100000000': '강원특별자치도',
    '4300000000': '충청북도',
    '4400000000': '충청남도',
    '5200000000': '전북특별자치도',
    '4700000000': '경상북도',
    '4800000000': '경상남도',
    '5000000000': '제주특별자치도'
}

# 지역명 추출 및 표준 컬럼명 부여
regions = []
for val in df.iloc[:, 0]:
    m = re.search(r'\((\d+)\)', str(val))
    code = m.group(1) if m else ''
    regions.append(code_to_region.get(code, '기타지역'))

df['지역명'] = regions
col_names = ['행정구역', '총인구수', '세대수', '세대당인구', '남자_인구수', '여자_인구수', '남여비율', '지역명']
df.columns = col_names

# 개별 시·도 비교를 위해 '전국' 총합 행 제외
df_regions = df[df['지역명'] != '전국'].copy().reset_index(drop=True)

# 숫자형 컬럼 쉼표(,) 제거 및 실수형(float) 변환
num_cols = ['총인구수', '세대수', '세대당인구', '남자_인구수', '여자_인구수', '남여비율']
for col in num_cols:
    df_regions[col] = df_regions[col].astype(str).str.replace(',', '').astype(float)

print("=" * 60)
print("1. 전처리된 주민등록 인구통계 데이터 요약")
print("=" * 60)
print(df_regions[['지역명', '총인구수', '세대수', '세대당인구', '남여비율']].head(10))

# ---------------------------------------------------------
# 2. 분석 변수 선정 및 표준화 (StandardScaler)
# ---------------------------------------------------------
# 인구 규모(총인구수, 세대수) 및 가구/성별 특성(세대당인구, 남여비율) 분석
features = ['총인구수', '세대수', '세대당인구', '남여비율']
X = df_regions[features]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
df_scaled = pd.DataFrame(X_scaled, columns=features)

print("\n" + "=" * 60)
print("2. 데이터 표준화 결과 (평균 0, 표준편차 1)")
print("=" * 60)
print(df_scaled.head())

# ---------------------------------------------------------
# 3. 주성분 분석 (PCA - 주성분 3개 적용)
# ---------------------------------------------------------
# 전체 변수 개수만큼 주성분 산출 (스크리 분석용)
pca_full = PCA(n_components=len(features))
pca_full.fit(df_scaled)

exp_var_full = pca_full.explained_variance_ratio_
cum_var_full = np.cumsum(exp_var_full)

print("\n" + "=" * 60)
print("3. 주성분별 설명 분산 비율 (Scree 분석)")
print("=" * 60)
for i, (ev, cv) in enumerate(zip(exp_var_full, cum_var_full), 1):
    print(f"PC{i}: 설명 분산 = {ev * 100:5.2f}% | 누적 설명 분산 = {cv * 100:5.2f}%")

# 주성분 3개(PC1, PC2, PC3)로 최종 변환
pca = PCA(n_components=3)
coords = pca.fit_transform(df_scaled)
pca_df = pd.DataFrame(coords, columns=['PC1', 'PC2', 'PC3'])
pca_df['지역명'] = df_regions['지역명']

exp_var = pca.explained_variance_ratio_
total_var = exp_var.sum()

print("\n" + "=" * 60)
print(f"주성분 3개 선정 시 누적 설명력: {total_var * 100:.2f}%")
print("=" * 60)

# 주성분별 변수 기여도(Loading) 확인
loadings = pd.DataFrame(pca.components_, columns=features, index=['PC1', 'PC2', 'PC3'])
print("주성분 부하량 (Loadings):")
print(loadings.round(3))
print("\n[주성분 의미 해석]")
print(f"- PC1 ({exp_var[0]*100:.1f}%): 총인구수(+0.650)와 세대수(+0.649)가 큼 -> '지역 인구 및 가구 규모'")
print(f"- PC2 ({exp_var[1]*100:.1f}%): 세대당 인구수(+0.954)가 압도적으로 큼 -> '가구 구성 규모 (가족 단위 중심 여부)'")
print(f"- PC3 ({exp_var[2]*100:.1f}%): 남여비율(+0.941)이 압도적으로 큼 -> '성비 특성 (남초/여초 비율)'")

# ---------------------------------------------------------
# 4. 결과 시각화 (스크리 플롯, 3차원 PCA 산점도, 로딩 막대 그래프)
# ---------------------------------------------------------
fig = plt.figure(figsize=(20, 6))

# (1) 왼쪽: 스크리 그림 (Scree Plot) - 2D
ax1 = fig.add_subplot(1, 3, 1)
x_indices = range(1, len(features) + 1)
pcs = [f'PC{i}' for i in range(1, len(features) + 1)]

ax1.bar(x_indices, exp_var_full * 100, color='#74C0FC', edgecolor='black', alpha=0.8, label='개별 설명 분산 (%)')
ax1.plot(x_indices, cum_var_full * 100, color='#E03131', marker='o', linewidth=2, markersize=7, label='누적 설명 분산 (%)')

for x, ev, cv in zip(x_indices, exp_var_full, cum_var_full):
    ax1.text(x, ev * 100 + 1.5, f'{ev * 100:.1f}%', ha='center', fontsize=9.5, fontweight='bold', color='#1864AB')
    ax1.text(x, cv * 100 + 2.0, f'{cv * 100:.1f}%', ha='center', fontsize=9.5, fontweight='bold', color='#C92A2A')

ax1.scatter([3], [cum_var_full[2] * 100], color='red', s=120, zorder=5, edgecolors='black')
ax1.annotate(f'3개 선정 (누적 {cum_var_full[2]*100:.1f}%)', xy=(3, cum_var_full[2] * 100), xytext=(2.1, 88),
             arrowprops=dict(facecolor='black', shrink=0.08, width=1, headwidth=6),
             fontsize=9.5, fontweight='bold')

ax1.set_xticks(list(x_indices))
ax1.set_xticklabels(pcs, fontsize=10.5)
ax1.set_ylim(0, 115)
ax1.set_xlabel('주성분 (Principal Component)', fontsize=11)
ax1.set_ylabel('설명 분산 비율 (%)', fontsize=11)
ax1.set_title('스크리 그림 (Scree Plot)', fontsize=12, fontweight='bold')
ax1.legend(loc='lower right', frameon=False, fontsize=9)
ax1.grid(axis='y', linestyle=':', alpha=0.6)
ax1.spines[['top', 'right']].set_visible(False)

# (2) 가운데: 3차원 PCA 산점도 (PC1, PC2, PC3 입체 공간)
ax2 = fig.add_subplot(1, 3, 2, projection='3d')
scatter = ax2.scatter(pca_df['PC1'], pca_df['PC2'], pca_df['PC3'],
                      c=pca_df['PC3'], cmap='coolwarm', s=90, edgecolors='black', alpha=0.9)

for _, row in pca_df.iterrows():
    ax2.text(row['PC1'], row['PC2'], row['PC3'] + 0.08,
             row['지역명'], fontsize=8.5, fontweight='semibold', ha='center')

ax2.set_xlabel(f'PC1 ({exp_var[0] * 100:.1f}%)\n[인구 규모]', fontsize=10, labelpad=8)
ax2.set_ylabel(f'PC2 ({exp_var[1] * 100:.1f}%)\n[가구당 인구]', fontsize=10, labelpad=8)
ax2.set_zlabel(f'PC3 ({exp_var[2] * 100:.1f}%)\n[남여 성비]', fontsize=10, labelpad=8)
ax2.set_title(f'3차원 PCA 공간 (누적: {total_var * 100:.1f}%)', fontsize=12, fontweight='bold', pad=15)
ax2.view_init(elev=20, azim=125)  # 보기 좋은 3D 각도로 회전

# (3) 오른쪽: 각 주성분별 변수 기여도 (PC1, PC2, PC3 Loading 막대 그래프)
ax3 = fig.add_subplot(1, 3, 3)
x_feat = np.arange(len(features))
width = 0.26
colors_load = ['#1C7ED6', '#F03E3E', '#20C997']
labels_load = [
    f'PC1 ({exp_var[0]*100:.1f}%): 인구 규모',
    f'PC2 ({exp_var[1]*100:.1f}%): 가구당 인구',
    f'PC3 ({exp_var[2]*100:.1f}%): 남여 성비'
]

for idx, pc_name in enumerate(['PC1', 'PC2', 'PC3']):
    ax3.bar(x_feat + (idx - 1) * width, loadings.loc[pc_name], width=width,
            color=colors_load[idx], label=labels_load[idx], edgecolor='black', alpha=0.85)

ax3.axhline(0, color='black', linewidth=0.8)
ax3.set_title('주성분별 변수 기여도 (PCA Loadings)', fontsize=12, fontweight='bold')
ax3.set_ylabel('부하량 (Loading)', fontsize=11)
ax3.set_xticks(x_feat)
ax3.set_xticklabels(features, rotation=0, fontsize=10.5)
ax3.set_ylim(-0.55, 1.15)
ax3.legend(frameon=True, facecolor='white', edgecolor='#dee2e6', loc='upper left', fontsize=9)
ax3.grid(axis='y', linestyle=':', alpha=0.6)
ax3.spines[['top', 'right']].set_visible(False)

plt.suptitle('주민등록 인구 데이터 주성분 분석 (PCA - 주성분 3개 종합 분석)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()

