import pandas as pd
# 도수분포표 작성
favorite = pd.Series(['WINTER', 'SUMMER', 'SPRING', 'SUMMER', 'SUMMER',
                      'FALL', 'FALL', 'SUMMER', 'SPRING', 'SPRING'])

print(f'\n[favorite] favorite의 내용 출력\n{favorite}')
print(f'\n[favorite.value_counts()] 도수분포 계산\n{favorite.value_counts()}')
print(f'\n[favorite.value_counts()/favorite.size] 비율 계산\n'
      f'{favorite.value_counts()/favorite.size}')

fd = favorite.value_counts()  # 도수분포를 fd에 저장
print(f'\n[type(fd)] fd의 자료구조 확인: {type(fd)}')
print(f"\n[fd['SUMMER']] SUMMER의 빈도 확인: {fd['SUMMER']}")
print(f'\n[fd.iloc[2]] 인덱스 2의 빈도 확인: {fd.iloc[2]}')
