with open('02_dev/frontend/search_result.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = "    kakao.maps.event.addListener(kakaoMap, 'click', () => infowindow.close());\n    kakaoMap.relayout();"
if old in content:
    print('이미 relayout 있음')
else:
    old2 = "    kakao.maps.event.addListener(kakaoMap, 'click', () => infowindow.close());"
    new2 = "    kakao.maps.event.addListener(kakaoMap, 'click', () => infowindow.close());\n    setTimeout(function(){ kakaoMap.relayout(); }, 100);"
    if old2 in content:
        content = content.replace(old2, new2, 1)
        print('relayout setTimeout 추가 완료')
    else:
        print('실패')

with open('02_dev/frontend/search_result.html', 'w', encoding='utf-8') as f:
    f.write(content)
