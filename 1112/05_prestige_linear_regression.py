# 회귀분석 과정: prestige 데이터로 직업별 소득을 예측하는 선형회귀 예제
import pandas as pd  # 데이터 처리 라이브러리
from sklearn.model_selection import train_test_split  # 훈련용·검증용 데이터 분리
from sklearn.linear_model import LinearRegression as LR  # 선형회귀 모델
from sklearn.metrics import mean_absolute_error as MAE  # 평균 절대 오차
import matplotlib.pyplot as plt  # 그래프 출력용 라이브러리
from pathlib import Path  # 파일 경로 처리용

# 이 파일의 위치를 기준으로 데이터 폴더를 찾는다(어느 폴더에서 실행해도 동작)
DATA_DIR = Path(__file__).resolve().parents[1] / 'data'

# 데이터 준비
df = pd.read_csv(DATA_DIR / 'prestige.csv')
print(df.head())

X = df[['education', 'women', 'prestige']]  # 독립변수: 평균 교육 연수, 여성 비율(%), 직업 위신 점수
y = df['income']  # 종속변수: 평균 소득

# 훈련용, 검증용 데이터 분리
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.3,  # 30%를 검증용으로 사용
    random_state=123)  # 실행할 때마다 같게 나뉘도록 고정

# 모델 생성
model = LR()
model.fit(X_train, y_train)  # 훈련용 데이터로 회귀식 계산

# 회귀식 확인: income = 계수1*education + 계수2*women + 계수3*prestige + 절편
print(model.coef_)  # 계수(독립변수 순서대로)
print(model.intercept_)  # 절편

# 모델 평가: MAE
pred = model.predict(X_test)  # 검증용 데이터의 소득 예측
print(MAE(y_test, pred))  # 실제값과 예측값 차이(절댓값)의 평균, 작을수록 좋음

# 실제값(x축)과 예측값(y축) 비교: 점이 대각선에 가까울수록 잘 예측한 것
plt.scatter(y_test, pred, color="red",)
plt.xlim([5000, 16000])
plt.ylim([5000, 16000])
plt.xlabel('y_test')
plt.ylabel('pred')
plt.plot(y_test, y_test, color='blue')  # 대각선 그리기
plt.show()

# 모델 활용
job = pd.DataFrame([[12, 10, 80]],  # 교육 연수 12년, 여성 비율 10%, 위신 점수 80인 직업
                   columns=X_test.columns)

print(job)
pred = model.predict(job)  # 이 직업의 예상 소득
print(pred)
