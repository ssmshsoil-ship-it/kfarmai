with open('02_dev/frontend/map.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 클러스터러 라이브러리 추가
old_sdk = 'dapi.kakao.com/v2/maps/sdk.js?appkey=533e5896630c1460c4349d33b3fab95a&autoload=false&libraries=services">'
new_sdk = 'dapi.kakao.com/v2/maps/sdk.js?appkey=533e5896630c1460c4349d33b3fab95a&autoload=false&libraries=services,clusterer">'

if old_sdk in content:
    content = content.replace(old_sdk, new_sdk, 1)
    print('SDK 클러스터러 라이브러리 추가 완료')
else:
    print('SDK 실패')

# 2. 마커 생성 후 클러스터러 적용
old_marker = '''    markers.forEach(function(marker) {
          marker.setMap(map);
        });'''

new_marker = '''    if (window.clusterer) {
          window.clusterer.clear();
        }
        window.clusterer = new kakao.maps.MarkerClusterer({
          map: map,
          averageCenter: true,
          minLevel: 5,
          disableClickZoom: false,
          styles: [{
            width: '40px', height: '40px',
            background: 'rgba(30,107,46,0.85)',
            borderRadius: '50%',
            color: '#fff',
            textAlign: 'center',
            fontWeight: 'bold',
            lineHeight: '40px',
            fontSize: '13px'
          }]
        });
        window.clusterer.addMarkers(markers);'''

if old_marker in content:
    content = content.replace(old_marker, new_marker, 1)
    print('클러스터러 적용 완료')
else:
    # 마커 setMap 방식 찾기
    import re
    pattern = r'markers\.forEach\(function\(marker\)\s*\{[^}]+marker\.setMap\(map\)[^}]+\}\);'
    match = re.search(pattern, content)
    if match:
        content = content[:match.start()] + new_marker + content[match.end():]
        print('regex로 클러스터러 적용 완료')
    else:
        print('클러스터러 실패 - 수동 확인 필요')

with open('02_dev/frontend/map.html', 'w', encoding='utf-8') as f:
    f.write(content)
