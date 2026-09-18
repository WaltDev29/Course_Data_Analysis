# 시리즈 객체의 복사
import pandas as pd

score_1 = pd.Series([80, 75, 90],
                    index=['KOR', 'ENG', 'MATH'])

score_2 = score_1  # score_1과 score_2는 동일한 객체
score_2.loc['KOR'] = 95
print(score_2)
print(score_1)

score_3 = score_1.copy()  # score_1과 score_3은 독립된 객체
score_3.loc['KOR'] = 70
print(score_3)
print(score_1)
