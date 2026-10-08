# plotly로 학생별 과목 점수 레이더 차트를 그리는 예제
# 실습전 라이브러리 설치
# pip install plotly
# pip install --upgrade "kaleido>=1"  (plotly 6 이상은 kaleido 1.0 이상 필요, PC에 Chrome 설치 필요)


import matplotlib.image as mpimg  # 이미지 파일 읽기용
import plotly.graph_objects as go  # plotly 그래프 객체 모듈
import pandas as pd  # 데이터 처리 라이브러리
import matplotlib.pyplot as plt  # 이미지 출력용 라이브러리
#####################################################################

# 레이더 차트 함수: df의 각 행을 하나의 다각형으로 그린다
# fills: 행별 채우기 방식, min_max: 축 값 범위, title: 그래프 제목
def radar(df, fills, min_max, title=''):
    fig = go.Figure()  # 빈 그래프 생성
    categories = df.columns.to_list()  # 컬럼명(과목)을 축 레이블로 사용
    categories.append(categories[0])  # 다각형을 닫기 위해 첫 레이블을 끝에 추가
    i = 0
    while (i < len(df)):  # 행(학생) 수만큼 반복
        scores = df.iloc[i, :].to_list()  # i번째 행의 점수 리스트
        scores.append(scores[0])  # 다각형을 닫기 위해 첫 점수를 끝에 추가
        fig.add_trace(go.Scatterpolar(
            r=scores,  # 축의 값
            theta=categories,  # 축의 레이블
            fill=fills[i],  # 다각형 채우기 색
            name=df.index[i]  # 다각형 레이블
        ))
        i += 1

        # 그래프 레이아웃 설정
        fig.update_layout(
            polar_radialaxis_visible=True,  # 방사형 축 표시
            polar_radialaxis_range=min_max,  # 축의 값 범위
            showlegend=True,  # 범례 표시
            margin_t=50,  # 상단 여백
            margin_l=100,  # 좌측 여백
            margin_r=100,  # 우측 여백
            margin_b=25,  # 하단 여백
            width=700,  # 그래프의 폭(pixel)
            height=700,  # 그래프의 높이(pixel)
            title_text=title,  # 그래프 제목
            title_font_size=30,  # 제목 폰트 사이즈
            font_size=20  # 폰트 사이즈
            )

    # 그래프 저장 & display
    plt.axis('off')  # 축 눈금 제거
    fig.write_image('radar.png')  # plotly 그래프를 png 파일로 저장(kaleido 필요)
    plt.imshow(mpimg.imread('radar.png'))  # 저장한 이미지를 읽어 matplotlib으로 표시
    plt.show()  # 그래프 화면에 출력
#####################################################################

# 데이터 입력
df = pd.DataFrame({
    'Kor': [72, 70, 90, 60, 66],
    'Eng': [84, 85, 95, 70, 85],
    'Math': [71, 40, 88, 80, 75],
    'Sci': [83, 80, 91, 90, 70],
    'Phy': [60, 60, 60, 70, 50]
})
df.index = ['AVG', 'John', 'Tom', 'Smith', 'Grace']  # 행 이름(평균 + 학생 4명)
print(df)  # 데이터 확인

# Smith와 평균 비교(평균은 선만, Smith는 내부 채우기)
fills = [None, 'toself']
radar(df=df.iloc[[0, 3], :],  # 0행(AVG)과 3행(Smith) 선택
      fills=fills,
      min_max=[0, 100],
      title='Scores of Smith'
      )

# 학생 4명 전체 비교(모두 내부 채우기)
fills = ['toself', 'toself', 'toself', 'toself']
radar(df=df.iloc[1:, :],  # AVG를 제외한 학생 행 선택
      fills=fills,
      min_max=[0, 100],
      title='Scores of Student'
      )
