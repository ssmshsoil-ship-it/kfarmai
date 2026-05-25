with open('02_dev/frontend/search_result.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = '''function renderMap(pestResults) {
  document.getElementById('mapPanel').style.display = 'block';
  const container = document.getElementById('resultMap');
  kakaoMap = new kakao.maps.Map(container, {
    center: new kakao.maps.LatLng(36.5, 127.8),
    level: 7
  });
  infowindow = new kakao.maps.InfoWindow({ zIndex:1 });
  kakao.maps.event.addListener(kakaoMap, 'click', () => infowindow.close());
  {'''

new = '''function renderMap(pestResults) {
  document.getElementById('mapPanel').style.display = 'block';
  kakao.maps.load(function() {
    const container = document.getElementById('resultMap');
    kakaoMap = new kakao.maps.Map(container, {
      center: new kakao.maps.LatLng(36.5, 127.8),
      level: 7
    });
    kakaoMap.relayout();
    infowindow = new kakao.maps.InfoWindow({ zIndex:1 });
    kakao.maps.event.addListener(kakaoMap, 'click', () => infowindow.close());
    {'''

if old in content:
    content = content.replace(old, new, 1)
    print('renderMap 복구 완료')
else:
    print('실패')

# 닫는 괄호 복구
old2 = '  }\n}\n\n/* ── 특정 마커 포커스 ── */'
new2 = '  });\n}\n\n/* ── 특정 마커 포커스 ── */'
if old2 in content:
    content = content.replace(old2, new2, 1)
    print('닫기 복구 완료')

with open('02_dev/frontend/search_result.html', 'w', encoding='utf-8') as f:
    f.write(content)
