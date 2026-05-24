with open('02_dev/frontend/map.html', 'r', encoding='utf-8') as f:
    content = f.read()

results = []

# 1. clusterer 라이브러리 이미 추가됨 확인
if 'clusterer' in content:
    results.append('라이브러리 OK')

# 2. clearMarkers에 클러스터러 초기화 추가
old1 = '''function clearMarkers() {
            markers.forEach(function(marker) { marker.setMap(null); });
            markers.length = 0;
            infowindow.close();
        }'''

new1 = '''let clusterer = null;
        function clearMarkers() {
            if (clusterer) { clusterer.clear(); }
            markers.forEach(function(marker) { marker.setMap(null); });
            markers.length = 0;
            infowindow.close();
        }'''

if old1 in content:
    content = content.replace(old1, new1, 1)
    results.append('clearMarkers 수정 완료')
else:
    results.append('clearMarkers 실패')

# 3. markers.push 이후 클러스터러 적용 - fitMapToBounds 호출 전에 추가
old2 = '''markers.push(marker);
            return marker;
        }
        function fitMapToBounds'''

new2 = '''markers.push(marker);
            return marker;
        }
        function applyClusterer() {
            if (clusterer) clusterer.clear();
            clusterer = new kakao.maps.MarkerClusterer({
                map: map,
                averageCenter: true,
                minLevel: 5,
                styles: [{
                    width: '42px', height: '42px',
                    background: 'rgba(30,107,46,0.9)',
                    borderRadius: '50%',
                    color: '#fff',
                    textAlign: 'center',
                    fontWeight: 'bold',
                    lineHeight: '42px',
                    fontSize: '13px'
                }]
            });
            clusterer.addMarkers(markers);
        }
        function fitMapToBounds'''

if old2 in content:
    content = content.replace(old2, new2, 1)
    results.append('applyClusterer 함수 추가 완료')
else:
    results.append('applyClusterer 실패')

# 4. fitMapToBounds 호출 후 applyClusterer 호출 추가
old3 = 'fitMapToBounds(activeList);'
new3 = 'fitMapToBounds(activeList);\n            applyClusterer();'

if old3 in content:
    content = content.replace(old3, new3, 1)
    results.append('applyClusterer 호출 완료')
else:
    results.append('applyClusterer 호출 실패')

with open('02_dev/frontend/map.html', 'w', encoding='utf-8') as f:
    f.write(content)

for r in results:
    print(r)
