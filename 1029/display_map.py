# folium 지도를 html 파일로 저장하고 웹 브라우저로 여는 보조 모듈
import webbrowser  # 웹 브라우저 열기용
import os  # 현재 작업 폴더 확인용

# 지도를 웹 브라우저에 표시
def showMap(map):
    map.save("map.html")  # 지도가 포함된 html 파일 생성
    filepath = os.getcwd()  # 현재 작업 폴더(html 파일이 저장된 곳)
    file_uri = 'file:///'+filepath + '/map.html'  # 브라우저에서 열 파일 주소
    webbrowser.open_new_tab(file_uri)  # html 파일 오픈