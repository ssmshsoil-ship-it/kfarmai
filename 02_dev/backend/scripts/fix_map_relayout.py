with open('02_dev/frontend/search_result.html', 'r', encoding='utf-8') as f:
    content = f.read()

# focusMarker에서 지도 relayout 추가
old = '''  if (!kakaoMap) return;
  kakaoMap.setCenter(new kakao.maps.LatLng(lat, lot));
  kakaoMap.setLevel(4);'''

new = '''  if (!kakaoMap) return;
  kakaoMap.relayout();
  kakaoMap.setCenter(new kakao.maps.LatLng(lat, lot));
  kakaoMap.setLevel(4);'''

if old in content:
    content = content.replace(old, new, 1)
    print('relayout 추가 완료')
else:
    print('실패 - 다른 방식 확인 필요')
    idx = content.find('focusMarker')
    print(content[idx:idx+300])

with open('02_dev/frontend/search_result.html', 'w', encoding='utf-8') as f:
    f.write(content)
