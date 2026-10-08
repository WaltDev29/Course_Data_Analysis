# 서울 기온 데이터로 월별 기온 분포 상자그림을 그리는 예제
import pandas as pd  # 데이터 처리 라이브러리
import seaborn as sns  # 통계 시각화 라이브러리
import matplotlib.pyplot as plt  # 그래프 출력용 라이브러리
from pathlib import Path  # 파일 경로 처리용

# 이 파일의 위치를 기준으로 데이터 폴더를 찾는다(어느 폴더에서 실행해도 동작)
DATA_DIR = Path(__file__).resolve().parents[2] / 'data'

df = pd.read_csv(DATA_DIR / 'seoul_temp.csv')  # 서울 일별 기온 데이터 읽기
print(df.head())  # 앞 5행 확인
df['month'] = (df.날짜 - 20230000) // 100  # 월 컬럼 생성(예: 20230315 → 315 → 3)
print(df.head())  # 월 컬럼이 추가되었는지 확인

# 그래프 테마 설정
sns.set_theme(style="white", rc={"figure.figsize": (7, 4)})  # 흰 배경(격자 없음), 그림 크기 7x4인치

# 월별 평균 기온에 의한 순위 계산
tmp = df.groupby('month').mean()  # 월별 평균값 계산
rank = tmp['평균기온'].rank() - 1  # 평균기온 순위(0부터 시작하도록 1을 뺌)
rank = rank.astype(int).to_list()  # 정수 리스트로 변환(색 인덱스로 사용)
print(rank)  # 순위 확인

# 팔레트 색 선택 및 순서 변경
mycolor = sns.color_palette('bwr', 12)  # 파랑(추움)→흰색→빨강(더움) 12단계 색
mycolor = pd.Series(mycolor)[rank].to_list()  # 기온 순위에 맞춰 각 월의 색을 재배치

# 월별 기온 분포를 상자그림으로 작성
plt.rcParams['font.family'] = 'Malgun Gothic'  # 한글 폰트 설정
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 부호 깨짐 방지

sns.boxplot(data=df,  # df 이름
            x='month',  # x축 컬럼
            y='평균기온',  # y축 컬럼
            hue='month',  # 그룹 지정
            legend=None,  # 범례 표시 안 함
            palette=mycolor  # 팔레트 지정
            ).set(title='월별 기온 분포')  # 그래프 제목

plt.ylabel('기온')  # y축 레이블
plt.subplots_adjust(bottom=0.2)  # 하단 여백
plt.show()  # 그래프 화면에 출력
