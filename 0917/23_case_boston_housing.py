# 코드 6-8: 보스턴 주택 데이터를 가격 그룹으로 나눠 분포와 변수 간 상관관계를 탐색하는 예제

# (0단계) 라이브러리 및 그래프 환경 설정
import pandas as pd
import matplotlib.pyplot as plt
# CategoricalDtype은 범주형 컬럼의 '값의 종류'와 '순서'를 직접 지정할 때 쓴다
from pandas.api.types import CategoricalDtype
from pathlib import Path

# 이 파일의 위치를 기준으로 데이터 폴더를 찾는다(어느 폴더에서 실행해도 동작)
DATA_DIR = Path(__file__).resolve().parents[1] / 'data'

# 그래프에 한글 표시 준비
# matplotlib의 기본 폰트에는 한글이 없어서 네모로 깨진다. 윈도우 기본 한글 폰트로 바꾼다
plt.rcParams['font.family'] = 'Malgun Gothic'
# 한글 폰트로 바꾸면 음수 기호가 깨지므로 유니코드 마이너스 사용을 끈다
plt.rcParams['axes.unicode_minus'] = False

# (1단계) 데이터 준비
df = pd.read_csv(DATA_DIR / 'BostonHousing.csv')
# 원본은 컬럼이 14개다. 분석에 쓸 5개만 남긴다
# crim=범죄율, rm=방 개수, dis=직업센터까지 거리, tax=재산세, medv=주택 가격
df = df[['crim', 'rm', 'dis', 'tax', 'medv']]
print(f'\n[df] 분석 대상 컬럼만 추출\n{df}')
# 그래프 축 레이블로 쓸 한글 이름. 위 컬럼 순서와 일치시켜야 한다
titles = ['1인당 범죄율', '방의 개수', '직업센터까지의 거리',
          '재산세', '주택 가격']

# (2단계) 그룹 컬럼 추가
# 주택 가격(medv)을 기준으로 전체를 H(상위)/M(중간)/L(하위) 세 그룹으로 나눈다
# 먼저 전부 'M'으로 채운 뒤, 조건에 맞는 행만 'H'와 'L'로 덮어쓰는 방식이다
grp = pd.Series(['M' for i in range(len(df))])
# loc에 조건식(True/False로 이루어진 시리즈)을 넣으면 True인 행만 골라 값을 바꾼다
grp.loc[df.medv >= 25.0] = 'H'
grp.loc[df.medv <= 17.0] = 'L'
df['grp'] = grp  # 만든 그룹 정보를 df의 새 컬럼으로 붙인다

# 그룹 컬럼의 자료형과 레이블 순서 변경
# 문자열(object)로 두면 정렬이 알파벳순(H, L, M)이 되어 그래프에 나오는 순서가 어색해진다
new_odr = ['H', 'M', 'L']  # 원하는 표시 순서
# ordered=True로 만들면 이 순서가 정렬과 대소 비교의 기준이 된다
new_dtype = CategoricalDtype(categories=new_odr, ordered=True)
df.grp = df.grp.astype(new_dtype)
print(f'\n[df.grp.dtype] 그룹 컬럼의 자료형: {df.grp.dtype}')

# (3단계) 데이터셋의 형태와 기본적인 내용 파악
print(f'\n[df.shape] 데이터셋의 형태: {df.shape}')
print(f'\n[df.head()] 데이터 앞부분 일부\n{df.head()}')
print(f'\n[df.dtypes] 컬럼별 자료형\n{df.dtypes}')
# sort=False면 빈도가 큰 순서가 아니라 위에서 지정한 H, M, L 순서로 나온다
print(f'\n[df.grp.value_counts(sort=False)] 주택 가격 그룹별 분포\n'
      f'{df.grp.value_counts(sort=False)}')

# (4단계) 히스토그램으로 관측값의 분포 확인
# 화면 분할 정의
# subplots()는 그림 하나(fig)와 그 안의 그래프 칸들(axes)을 함께 만든다
# axes는 2행 3열짜리 격자이므로 axes[행, 열] 형태로 칸을 지정한다
fig, axes = plt.subplots(nrows=2, ncols=3)
fig.subplots_adjust(hspace=0.5, wspace=0.3)  # 그래프 여백

# 각 분할 영역에 그래프 작성하기
# 컬럼 5개를 칸 6개에 차례로 채운다. i//3이 행 번호, i%3이 열 번호가 된다
# i=0은 [0,0], i=1은 [0,1], i=3은 [1,0]에 들어가고 마지막 한 칸은 비어 있다
for i in range(5):
    # ax=에 칸을 넘기면 새 창이 아니라 그 칸 안에 그래프가 그려진다
    df[df.columns[i]].plot.hist(ax=axes[i//3, i % 3],
                                ylabel='', xlabel=titles[i])

# 통합 그래프에 제목 지정
fig.suptitle('Histogram', fontsize=14)

# 분할 그래프 화면에 나타내기
fig.show()

# (5단계) 상자그림으로 관측값의 분포 확인
# 상자그림은 사분위수와 이상치를 같이 보여줘서 히스토그램이 놓치는 치우침을 드러낸다
fig, axes = plt.subplots(nrows=2, ncols=3)  # 앞의 fig를 덮어쓰고 새 그림을 만든다
fig.subplots_adjust(hspace=0.5, wspace=0.3)  # 그래프 여백

# 각 분할 영역에 그래프 작성하기
for i in range(5):
    df[df.columns[i]].plot.box(ax=axes[i//3, i % 3],
                               label=titles[i])

fig.suptitle('Boxplot', fontsize=14)
fig.show()

# (6단계) 그룹별 관측값의 분포 확인
# 5단계가 전체 분포였다면 여기서는 H/M/L 그룹별로 나눠 그려 그룹 간 차이를 비교한다
fig, axes = plt.subplots(nrows=2, ncols=3)
fig.subplots_adjust(hspace=0.5, wspace=0.3)  # 그래프 여백

# 각 분할 영역에 그래프 작성하기
for i in range(5):
    # by='grp'를 주면 grp 값별로 상자를 따로 그려준다
    df.boxplot(column=df.columns[i], by='grp', grid=False,
               ax=axes[i//3, i % 3], xlabel=titles[i])

fig.suptitle('Boxplot by group', fontsize=14)
fig.show()

# (7단계) 다중 산점도를 통한 변수 간 상관관계의 확인
# scatter_matrix는 변수들을 둘씩 짝지어 산점도를 격자 형태로 한 번에 그린다
# iloc[:, :5]로 앞의 숫자 컬럼 5개만 넘긴다(grp는 문자라 산점도를 그릴 수 없다)
pd.plotting.scatter_matrix(df.iloc[:, :5])
plt.show()

# (8단계) 그룹 정보를 포함한 변수 간 상관관계의 확인
# 점의 색으로 그룹을 구분하면 그룹별로 점이 어떻게 갈라지는지 한눈에 보인다
# 참고: dict은 파이썬 내장 함수 이름이라 변수명으로 쓰면 이후 dict()를 호출할 수 없다
dict = {'H': 'red', 'M': 'green', 'L': 'gray'}
# 각 행의 grp 값을 색 이름으로 바꿔서 행 개수만큼의 색 리스트를 만든다
colors = list(dict[key] for key in df.grp)  # 각 점의 색을 지정
pd.plotting.scatter_matrix(df.iloc[:, :5], c=colors)
plt.show()

# (9단계) 변수 간 상관계수의 확인
# corr()는 피어슨 상관계수를 계산한다. 1에 가까우면 같은 방향, -1에 가까우면 반대 방향이다
print(f'\n[df.iloc[:, :5].corr()] 변수 간 상관계수\n'
      f'{df.iloc[:, :5].corr()}')
