with open('02_dev/frontend/search_result.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = '''    if (!kakaoMap) {
      kakaoMap = new kakao.maps.Map(container, {
        center: new kakao.maps.LatLng(36.5, 127.8),
        level: 7
      });
      infowindow = new kakao.maps.InfoWindow({ zIndex:1 });
      kakao.maps.event.addListener(kakaoMap, 'click', () => infowindow.close());
    }'''

new = '''    kakaoMap = new kakao.maps.Map(container, {
      center: new kakao.maps.LatLng(36.5, 127.8),
      level: 7
    });
    infowindow = new kakao.maps.InfoWindow({ zIndex:1 });
    kakao.maps.event.addListener(kakaoMap, 'click', () => infowindow.close());
    kakaoMap.relayout();'''

if old in content:
    content = content.replace(old, new, 1)
    print('kakaoMap 재초기화 완료')
else:
    print('실패')

with open('02_dev/frontend/search_result.html', 'w', encoding='utf-8') as f:
    f.write(content)
