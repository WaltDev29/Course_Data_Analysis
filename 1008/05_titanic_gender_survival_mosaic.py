# 타이타닉 데이터로 성별 생존비율 모자이크 플롯을 그리는 예제
import matplotlib.pyplot as plt  # 그래프 출력용 라이브러리
import seaborn as sns  # 데이터셋 불러오기용
from statsmodels.graphics.mosaicplot import mosaic  # 모자이크 플롯 함수

plt.rcParams['font.family'] = 'Malgun Gothic'  # 한글 폰트 설정
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 부호 깨짐 방지

# 데이터 준비
df = sns.load_dataset('titanic')  # seaborn 내장 타이타닉 승객 데이터 불러오기
print(df.head())  # 앞 5행 확인
dict1 = {0: '사망', 1: '생존'}  # 생존 여부 코드 → 한글 변환표
dict2 = {'male': '남성', 'female': '여성'}  # 성별 영문 → 한글 변환표
df = df.replace({'survived': dict1})  # survived 컬럼 값을 한글로 변환
df = df.replace({'sex': dict2})  # sex 컬럼 값을 한글로 변환
print(df.head())  # 변환 결과 확인

# 그래프 설정
def props(key):  # key: 각 타일의 범주 조합(예: ('남성', '생존'))
       return {'color': 'lightgreen' if '생존' in key else 'yellow'}  # 생존은 연두색, 사망은 노란색

# 그래프 작성
mosaic(data=df.sort_values('sex'),  # 성별 순으로 정렬한 데이터
       index=['sex', 'survived'],  # 1차 분할: 성별, 2차 분할: 생존 여부
       properties=props,  # 타일 색상 변경
       axes_label=True,  # 축 레이블 표시
       title='타이타닉 남녀 생존비율'  # 그래프 제목
       )

plt.show()  # 그래프 화면에 출력
