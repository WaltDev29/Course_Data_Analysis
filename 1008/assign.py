import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.graphics.mosaicplot import mosaic  # 모자이크 플롯 함수

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

df = pd.read_csv(DATA_DIR / "krx_20261007.csv", encoding="cp949")

sns.set_theme(style="whitegrid")  # 흰 배경+격자
plt.rcParams['font.family'] = 'Malgun Gothic'  # 한글 폰트 설정
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 부호 깨짐 방지

# ============ 데이터 기본 정보 ============
print("데이터 크기", df.shape)
print("\n컬럼: ", list(df.columns))
# print(df.info())
print("\n", df.head())
print("\n", df["시장구분"].value_counts())

df = df.sort_values("시가총액", ascending=False).reset_index(drop=True)
df.loc[df["대비"] > 0, "등락"] = "상승"
df.loc[df["대비"] == 0, "등락"] = "보합"
df.loc[df["대비"] < 0, "등락"] = "하락"

# ============ 데이터 시각화 ============

# 가로 막대 그래프
sns.barplot(data=df[:15], x="시가총액", y="종목명")
plt.tight_layout()
plt.show()


# 버블차트
palette = {
    "상승": "red",
    "보합": "gray",
    "하락": "blue"
}

sns.scatterplot(
    data=df[:30],  # df 이름
    x="등락률",  # x축
    y="거래대금",  # y축
    size="시가총액",  # 원의 크기
    sizes=(100, 4000),  # 원의 크기 범위
    hue="등락",
    palette=palette,
    alpha=0.5,  # 투명도
    legend=False  # 범례 표시 여부
)

# 종목명을 버블 위에 표시
for i in range(0, 30):
    plt.text(x=df["등락률"][i], y=df["거래대금"][i], s=df["종목명"][i],  # 버블 중심 좌표에 주 이름 출력
         horizontalalignment='center', size='small', color='dimgray')  # 가운데 정렬, 작은 회색 글씨
plt.show() 


# 모자이크 플롯
def props(key):
       return {'color': 'red' if '상승' in key else ('blue' if '하락' in key else 'gray')}

df_temp = df[df["시장구분"].isin(["KOSPI", "KOSDAQ"])].copy()

mosaic(data=df_temp,
       index=['시장구분', '등락'],
       properties=props,  # 타일 색상 변경       
       axes_label=True,  # 축 레이블 표시
       )

plt.show()  # 그래프 화면에 출력


# 히트맵
# 피벗 테이블 생성
df_temp = df.pivot_table(index='시장구분',  # 행 위치에 들어갈 컬럼
                         columns='소속부',  # 열 위치에 들어갈 컬럼
                         values='등락률',  # 데이터로 사용할 컬럼
                         aggfunc='mean'  # 데이터 집계함수
                         )
print(df.head())  # 피벗 결과 확인(행: 월, 열: 연도)

# 히트맵 작성
sns.set_theme(rc={'figure.figsize': (8, 7)})  # 그림 크기 8x7인치
sns.heatmap(df).set_title('Heatmap of Flight Passenger', fontsize=20)  # 값이 클수록 밝은 색으로 표시, 제목 지정
plt.show()  # 그래프 화면에 출력
